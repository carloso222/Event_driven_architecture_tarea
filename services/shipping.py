from common.broker import consume, publish
from common.events import create_event

SERVICE = "shipping-service"


def handle(channel, event):
    publish(channel, create_event("order_shipped", SERVICE, event["payload"]))


consume(SERVICE, ["order_fulfilled"], handle)
