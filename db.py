"""Shared MongoDB connection helper for consumer.py and analytics.py."""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "student_activity_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "student_events")


def get_collection():
    if not MONGO_URI or "<db_password>" in MONGO_URI:
        raise RuntimeError(
            "MONGO_URI is not set. Copy .env.example to .env and fill in the "
            "real MongoDB Atlas password."
        )
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION]
