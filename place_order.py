import uuid

from common.broker import connect, publish
from common.events import create_event

order = {
    "order_id": str(uuid.uuid4())[:8],
    "book": "Fundamentals of Software Architecture",
    "quantity": 1,
    "price": 899.0,
}

connection, channel = connect()
publish(channel, create_event("place_order", "app", order))
connection.close()
