import json

import pika

from app.core.config import settings

params = pika.URLParameters(
    f"{settings.RABBITMQ_URL}?heartbeat={settings.HEARTBEAT}&connection_attempts={settings.CONNECTION_ATTEMPTS}&retry_delay={settings.RETRY_DELAY}"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="accounting",
        body=json.dumps(body),
        properties=properties,
    )
