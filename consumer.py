"""Kafka Consumer - reads student activity events from Kafka, displays
them, and stores them in MongoDB.
"""

import json
import os

from dotenv import load_dotenv
from kafka import KafkaConsumer

from db import get_collection

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "student_activities")

# Stop after this many seconds of silence, so the script can be run and
# graded without needing a manual Ctrl+C once the producer is done.
IDLE_TIMEOUT_MS = int(os.getenv("CONSUMER_IDLE_TIMEOUT_MS", "10000"))


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="student-activity-consumer-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=IDLE_TIMEOUT_MS,
    )
    collection = get_collection()

    print(f"Connected to Kafka at {BOOTSTRAP_SERVERS}, subscribed to '{TOPIC}'.")
    print("Connected to MongoDB. Waiting for events...")

    message_counter = 0
    try:
        for message in consumer:
            event = message.value
            collection.insert_one(dict(event))
            message_counter += 1
            print(f"Event: {event} | Total messages consumed: {message_counter}")
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        consumer.close()
        print(f"Done. Total messages consumed and stored: {message_counter}")


if __name__ == "__main__":
    main()
