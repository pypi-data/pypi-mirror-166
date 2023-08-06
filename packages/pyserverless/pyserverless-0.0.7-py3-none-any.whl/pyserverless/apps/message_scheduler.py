import json
import time
from threading import Thread
from typing import Dict
from urllib.parse import quote_plus

import codefast as cf

from pyserverless.const import Const


class Channel(object):
    def post(self, content: str) -> bool:
        print(content)
        url = Const.bark.host.replace(
            'ServerAlerts', 'scheduled message') + quote_plus(content)
        url += '?icon=https://file.ddot.cc/tmp/logo_apple.png'
        cf.net.get(url)


class ScheduledMessage(object):
    # Post a message after a few seconds
    def __init__(self, message_body: Dict, channel: Channel,
                 redis_key: str) -> None:
        self.message_body = message_body
        self.seconds = message_body.get('seconds', 30)
        self.content = message_body.get('content', 'sheduled message')
        self.channel = channel
        self.redis_key = redis_key
        self.sleep_period = 3

    def run(self) -> None:
        cf.info('posting message {} in {} seconds'.format(
            self.content, self.seconds))
        time.sleep(self.sleep_period)
        self.seconds -= self.sleep_period
        if self.seconds <= 0:
            self.channel.post(self.content)
            cf.info('Scheduled message posted:', self.content)
        else:  # put message back
            Const.redis.rpush(
                self.redis_key,
                json.dumps({
                    'scheduled_message': {
                        'seconds': self.seconds,
                        'content': self.content
                    }
                }))
            cf.info('Scheduled message put back:', self.content)


def poster():
    key = "blackhole_list"
    missing = 0
    while True:
        try:
            _, b = Const.redis.blpop(key)
            js = json.loads(b.decode())
            cf.info(js)
            message_body = js.get('scheduled_message', {})
            if message_body:
                cf.info('Run once task:', message_body)
                sm = ScheduledMessage(message_body, Channel(), key)
                t = Thread(target=sm.run)
                t.start()
            else:
                missing += 1
                Const.redis.rpush(key, b)

            if missing > 10:
                cf.info('Missing tasks:', missing)
                time.sleep(1)
                missing = 0
        except Exception as e:
            cf.error(e)
