import os
import json
from pathlib import Path

import click
from elasticsearch5 import Elasticsearch, helpers

from utils import convert_message

ELASTICSEARCH_URL = os.environ['ELASTICSEARCH_URL']
es = Elasticsearch([ELASTICSEARCH_URL])


INDEX_NAME = 'slack'
TYPE_NAME = 'message'


@click.group()
def cmd():
    pass


def parse_file(fname, channel):
    results = []
    for data in json.load(fname.open()):
        data = convert_message(data)
        if data is None:
            continue

        data['channel'] = channel
        results.append(data)
        print(data)
    return results


def parse_dir(path, channel2id):
    channel_name = path.name
    channel = channel2id[channel_name]
    actions = []
    for fname in path.iterdir():
        for data in parse_file(fname, channel):
            act = {'_index': INDEX_NAME, '_type': TYPE_NAME}
            act['_source'] = data
            actions.append(act)

    print(channel_name, len(actions))
    helpers.bulk(es, actions)


@cmd.command()
@click.option('--slack_dir', default='slack')
def import_json(slack_dir):
    channels = json.load(Path(slack_dir).joinpath('channels.json').open())
    channel2id = dict((x['name'], x['id']) for x in channels)

    slack_dir = Path(slack_dir)
    for path in slack_dir.iterdir():
        if not path.is_dir():
            continue
        parse_dir(path, channel2id)


@cmd.command()
@click.option('--config_file', default='config.json')
def make_index(config_file):
    body = json.load(open(config_file))
    es.indices.create(index=INDEX_NAME, body=body)


if __name__ == '__main__':
    cmd()
