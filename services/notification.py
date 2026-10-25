from common.broker import consume, publish
from common.events import create_event

SERVICE = "notification-service"


def handle(channel, event):
    publish(channel, create_event("email_sent", SERVICE, event["payload"]))


consume(SERVICE, ["order_placed", "order_fulfilled", "order_shipped"], handle)
