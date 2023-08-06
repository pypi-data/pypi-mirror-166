import random
import threading
import time

import codefast as cf

from .rabbitmq import Consumer, Publisher

AMQP_URL = "~/.config/amqp.json"


def publish_message(msg: str, publisher: Publisher):
    publisher.post(msg)


def loop_publish_message(publisher: Publisher):
    while True:
        try:
            msg = cf.random_string(1024)
            cf.info("[-] publishing", msg)
            publisher.publish(str(msg))
            time.sleep(random.randint(1, 30))
        except Exception as e:
            cf.error(e)
            time.sleep(1)


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    cf.info("[-] processing", body.decode())


def consume_message(consumer: Consumer, callback: callable):
    try:
        consumer.consume(callback)
    except Exception as e:
        cf.error(e)


def eloop():
    publisher = Publisher(AMQP_URL, "test")
    consumer = Consumer(AMQP_URL, "test")
    c = threading.Thread(target=consume_message, args=(consumer, callback))
    p = threading.Thread(target=loop_publish_message, args=(publisher, ))
    c.start()
    p.start()


if __name__ == "__main__":
    eloop()
