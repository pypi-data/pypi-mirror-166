# example_publisher.py
import codefast as cf
import pika


class Connector(object):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        params = pika.URLParameters(amqp_url)
        params.socket_timeout = 5
        connection = pika.BlockingConnection(params)

        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue_name)


class Publisher(Connector):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        super().__init__(amqp_url.strip(), queue_name.strip())

    def post(self, msg: str) -> None:
        # Alias of self.publish
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=msg)
        cf.info("{} sent to {}".format(msg, self.queue_name))
        return

    def publish(self, msg: str) -> None:
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=msg)
        cf.info("{} sent to {}".format(msg, self.queue_name))
        return


class Consumer(Connector):
    def __init__(self, amqp_url: str, queue_name: str) -> None:
        super().__init__(amqp_url, queue_name)
        self.channel.basic_qos(prefetch_count=10)
        return

    def consume(self, callback: callable) -> None:
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=callback,
                                   auto_ack=True)
        cf.info("Start consuming messages. To exit press CTRL+C")
        self.channel.start_consuming()
        return


from authc import gunload


class AMQPPublisher(Publisher):
    def __init__(self, queue_name: str) -> None:
        URL = gunload('amqp_url')
        super().__init__(URL, queue_name)


class AMQPConsumer(Consumer):
    def __init__(self, queue_name: str) -> None:
        URL = gunload('amqp_url')
        super().__init__(URL, queue_name)


def post_message_to_queue(msg: str, queue_name: str) -> None:
    AMQPPublisher(queue_name).post(msg)
