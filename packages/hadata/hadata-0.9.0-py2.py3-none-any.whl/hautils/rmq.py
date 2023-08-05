import os
import pika
from pika import PlainCredentials
from dotenv import load_dotenv

from hautils.logger import logger

load_dotenv(override=False)

RABBIT_MQ_HOST = os.getenv('RABBIT_MQ_HOST')
RABBIT_MQ_USER = os.getenv("RABBIT_MQ_USER")
RABBIT_MQ_PASS = os.getenv("RABBIT_MQ_PASS")


def get_rmq_connection():
    logger.log("connecting to rmq %s - %s - %s" % (RABBIT_MQ_HOST, RABBIT_MQ_USER, RABBIT_MQ_PASS))
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_MQ_HOST,
                                  credentials=PlainCredentials
                                  (RABBIT_MQ_USER, RABBIT_MQ_PASS)))


def publish_rmq(exchange, body, ex_type="direct"):
    connection = get_rmq_connection()
    channel = connection.channel()
    logger.info("publishing to exchange %s with data %s" % (exchange, body))
    channel.exchange_declare(exchange=exchange, exchange_type=ex_type)
    channel.basic_publish(exchange=exchange, routing_key='', body=body)
    connection.close()
    logger.info("closing connection")


def rmq_bind(exchange="ha", queue="ha"):
    logger.log("binding queues together %s to %s" % (exchange, queue))
    connection = get_rmq_connection()
    channel = connection.channel()
    result = channel.queue_declare(queue=queue, exclusive=True)
    logger.log("queue declare result %s" % (result,))
    result = channel.queue_bind(exchange=exchange,
                                queue=queue)
    logger.log("queue bind result %s" % (result,))
