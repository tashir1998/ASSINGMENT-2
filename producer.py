"""Kafka Producer - generates student activity events and publishes them
to the `student_activities` Kafka topic.
"""

import json
import random
import time
from datetime import datetime, timezone

from kafka import KafkaProducer

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "student_activities"
EVENT_COUNT = 1000
DELAY_SECONDS = 0.01

ACTIVITY_TYPES = [
    "login",
    "view_material",
    "assignment_submission",
    "quiz_completion",
]
STUDENT_IDS = [f"STU{i:03d}" for i in range(1, 51)]
COURSE_IDS = [f"CRS{i:03d}" for i in range(101, 111)]


def build_event():
    return {
        "student_id": random.choice(STUDENT_IDS),
        "course_id": random.choice(COURSE_IDS),
        "activity_type": random.choice(ACTIVITY_TYPES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}. Sending {EVENT_COUNT} "
          f"events to topic '{KAFKA_TOPIC}'...")

    for i in range(1, EVENT_COUNT + 1):
        event = build_event()
        producer.send(KAFKA_TOPIC, value=event)
        print(f"[{i}/{EVENT_COUNT}] Sent: {event}")
        if DELAY_SECONDS:
            time.sleep(DELAY_SECONDS)

    producer.flush()
    producer.close()
    print("All events sent and flushed.")


if __name__ == "__main__":
    main()
