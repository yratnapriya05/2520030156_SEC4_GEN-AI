
# mongo_logger.py

import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "llm_monitoring"
)

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

collection = db["call_logs"]


def log_call(
    provider,
    model,
    prompt,
    response,
    input_tokens=0,
    output_tokens=0,
    cost=0.0
):
    log_data = {
        "provider": provider,
        "model": model,
        "prompt": prompt,
        "response": response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost,
        "timestamp": datetime.now(timezone.utc)
    }

    result = collection.insert_one(log_data)

    return str(result.inserted_id)


def close_connection():
    client.close()
