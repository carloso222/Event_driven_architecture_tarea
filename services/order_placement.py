from common.broker import consume, publish
from common.events import create_event

SERVICE = "order-placement-service"


def handle(channel, event):
    publish(channel, create_event("order_placed", SERVICE, event["payload"]))


consume(SERVICE, ["place_order"], handle)
