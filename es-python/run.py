import os
import time
from datetime import datetime

import click
from slackclient import SlackClient
from elasticsearch5 import Elasticsearch, helpers

from utils import convert_message
from config import INDEX_NAME, TYPE_NAME

ELASTICSEARCH_URL = os.environ['ELASTICSEARCH_URL']
es = Elasticsearch([ELASTICSEARCH_URL])

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)


@click.group()
def cmd():
    pass


def fetch_message(es, channel, timestamp):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "timestamp": timestamp
                        }
                    },
                    {
                        "match": {
                            "channel": channel
                        }
                    }
                ],
            }
        }
    }
    res = es.search(index='slack', body=body)
    return res['hits']


@cmd.command()
def batch():
    ret = sc.api_call('channels.list')
    channels = ret['channels']
    channels = [(c['id'], c['name']) for c in channels]

    for channel_id, channel_name in channels:
        print('channel = ', channel_name)
        count = 100
        latest = str(datetime.now().timestamp())
        has_more = True
        actions = []

        while has_more:
            ret = sc.api_call(
                "channels.history",
                channel=channel_id,
                count=count,
                latest=latest
            )
            print(ret['ok'], ret.get('error', ''))
            has_more = ret['has_more']
            if not has_more:
                break

            messages = ret['messages']
            latest = messages[-1]['ts']

            for data in messages:
                data = convert_message(data)
                if data is None:
                    continue
                data['channel'] = channel_id

                res_msg = fetch_message(es, data['channel'], data['timestamp'])
                if res_msg['total'] != 0:
                    assert res_msg['total'] == 1
                    continue

                act = {'_index': INDEX_NAME, '_type': TYPE_NAME}
                act['_source'] = data
                actions.append(act)

        print(channel_name, len(actions))
        helpers.bulk(es, actions)
        time.sleep(1)


if __name__ == '__main__':
    cmd()
