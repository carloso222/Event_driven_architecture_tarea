from common.broker import consume, publish
from common.events import create_event

SERVICE = "payment-service"


def handle(channel, event):
    publish(channel, create_event("payment_applied", SERVICE, event["payload"]))


consume(SERVICE, ["order_placed"], handle)
