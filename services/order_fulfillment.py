from common.broker import consume, publish
from common.events import create_event

SERVICE = "order-fulfillment-service"


def handle(channel, event):
    publish(channel, create_event("order_fulfilled", SERVICE, event["payload"]))


consume(SERVICE, ["payment_applied"], handle)
