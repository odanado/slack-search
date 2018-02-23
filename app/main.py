# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals

import os
import uuid
import logging
import traceback
from time import strftime
from urllib.parse import urlencode
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler


from elasticsearch5 import Elasticsearch

import flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import jwt


SLACK_OAUTH_URL = 'https://slack.com/api/oauth.access'

SLACK_CLIENT_ID = os.environ['SLACK_CLIENT_ID']
SLACK_CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']

CLIENT_URL = os.environ['CLIENT_URL']
CLIENT_REDIRECT_URL = CLIENT_URL + '/auth/signed-in'
SECRET_KEY = os.environ['SECRET_KEY']

ELASTICSEARCH_URL = os.environ['ELASTICSEARCH_URL']

POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

app = flask.Flask(__name__)
cors = CORS(app, resources={
    r"/validate_token": {"origins": CLIENT_URL},
    r"/search": {"origins": CLIENT_URL}
})

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:{}@db'.format(POSTGRES_PASSWORD)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

es = Elasticsearch([ELASTICSEARCH_URL])


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), index=True, unique=True)
    secret = db.Column(db.String(36), unique=True)

    def to_dict(self):
        return dict(
            id=self.id,
            token=self.token,
            secret=self.secret
        )

    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def __repr__(self):
        return '<Model {}>'.format(self.token)


def findToken(token):
    reason = ''

    user = db.session.query(User).filter(User.token == token).first()
    if user is None:
        reason = 'not authorized'
        return None, reason

    try:
        decoded_token = jwt.decode(token, SECRET_KEY)
    except jwt.exceptions.DecodeError:
        reason = 'invalid token'
        return None, reason

    if 'access_token' not in decoded_token['slack']:
        reason = 'invalid slack token'
        return None,  reason

    return user, reason


@app.route('/search')
def search():
    text = flask.request.args['text']
    token = flask.request.args['token']

    user, reason = findToken(token)
    if user is None:
        return flask.jsonify({'status': 'error', 'reason': reason})

    body = {
        "query": {
            "match_phrase": {
                "text": text
            }
        },
        "sort": {"timestamp": {"order": "desc"}}
    }
    res = es.search(index='slack', doc_type='message', body=body)
    results = [x['_source'] for x in res['hits']['hits']]

    return flask.jsonify({
        'status': 'ok',
        'results': results
    })


@app.route('/validate_token')
def validate_token():
    token = flask.request.args['token']
    user, reason = findToken(token)
    if user is None:
        return flask.jsonify({'status': 'error', 'reason': reason})

    return flask.jsonify({
        'status': 'ok',
        'secret': user.secret
    })


@app.route('/callback')
def callback():
    if 'code' in flask.request.args:
        response = requests.get(
            SLACK_OAUTH_URL,
            params={
                'client_id': SLACK_CLIENT_ID,
                'client_secret': SLACK_CLIENT_SECRET,
                'code': flask.request.args['code'],
                'redirect_uri': flask.url_for('.callback', _external=True),
            })
        args = {
            'slack': response.json(),
            'access_token': str(uuid.uuid4()),
            'expiry': (datetime.now() + timedelta(days=14)).timestamp(),
        }
        token = jwt.encode(args, SECRET_KEY)
        # bytes -> str
        token = token.decode()
        secret = flask.request.args['state']
        params = {
            'token': token,
            'secret': secret
        }

        if findToken(token)[0] is None:
            user = User(token, secret)
            db.session.add(user)
            db.session.commit()

        redirect_url = '{}?{}'.format(
            CLIENT_REDIRECT_URL,
            urlencode(params),
        )
        return flask.redirect(redirect_url)

    return ''


@app.after_request
def after_request(response):
    # This IF avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                     ts,
                     flask.request.remote_addr,
                     flask.request.method,
                     flask.request.scheme,
                     flask.request.full_path,
                     response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 ts,
                 flask.request.remote_addr,
                 flask.request.method,
                 flask.request.scheme,
                 flask.request.full_path,
                 tb)
    return "Internal Server Error", 500


if __name__ == '__main__':
    handler = RotatingFileHandler(
        'logs/app.log', maxBytes=5 * 1024 * 1024)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)

    db.create_all()
    db.session.commit()
    app.run(host='0.0.0.0')
