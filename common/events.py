import uuid
from datetime import datetime, timezone


def create_event(event_type, producer, payload):
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "producer": producer,
        "payload": payload,
    }
