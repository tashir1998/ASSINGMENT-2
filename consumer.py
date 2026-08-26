"""Kafka Consumer - reads student activity events from Kafka, displays
them, and stores them in MongoDB.
"""

import json

from kafka import KafkaConsumer
from pymongo import MongoClient

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "student_activities"

# TODO: replace <db_password> with the real password for fatehanasrin7976_db_user
MONGO_URI = "mongodb+srv://fatehanasrin7976_db_user:<db_password>@cluster0.idqmng1.mongodb.net/?appName=Cluster0"
MONGO_DB_NAME = "student_activity_db"
MONGO_COLLECTION = "student_events"

# Stop after this many seconds of silence, so the script can be run and
# graded without needing a manual Ctrl+C once the producer is done.
IDLE_TIMEOUT_MS = 10000


def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="student-activity-consumer-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=IDLE_TIMEOUT_MS,
    )

    mongo_client = MongoClient(MONGO_URI)
    collection = mongo_client[MONGO_DB_NAME][MONGO_COLLECTION]

    print(f"Connected to Kafka at {KAFKA_BOOTSTRAP_SERVERS}, subscribed to "
          f"'{KAFKA_TOPIC}'.")
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
        mongo_client.close()
        print(f"Done. Total messages consumed and stored: {message_counter}")


if __name__ == "__main__":
    main()
