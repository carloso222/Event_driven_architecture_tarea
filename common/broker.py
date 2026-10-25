import json
import os

import pika

EXCHANGE = "events"


def connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq")))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")
    return connection, channel


def log(service, action, event_type):
    print(f"{service} - {action} - {event_type}", flush=True)


def publish(channel, event):
    channel.basic_publish(exchange=EXCHANGE, routing_key=event["event_type"], body=json.dumps(event))
    log(event["producer"], "produced", event["event_type"])


def consume(service, event_types, handler):
    """Escucha los event_types indicados y llama handler(channel, event) por cada evento."""
    connection, channel = connect()
    channel.queue_declare(queue=service)
    for event_type in event_types:
        channel.queue_bind(queue=service, exchange=EXCHANGE, routing_key=event_type)

    def callback(ch, method, properties, body):
        event = json.loads(body)
        log(service, "consumed", event["event_type"])
        handler(ch, event)

    channel.basic_consume(queue=service, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
