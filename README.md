# Student Activity Monitoring System (Apache Kafka + MongoDB)

Simulates student activity events (login, view_material, assignment_submission,
quiz_completion) flowing from a Kafka producer to a Kafka consumer that stores
them in MongoDB, plus analytics and a bar chart visualization.

## 1. Start Kafka (local install, no Docker)

Requires a JDK (Java 11+) installed and on your `PATH` (`java -version` to check).

**Download & extract** (Linux/macOS shown; on Windows download the same
`.tgz` from https://kafka.apache.org/downloads and extract it, then use the
`.bat` scripts under `bin\windows\` instead of `bin/*.sh` below):

```bash
curl -O https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
tar -xzf kafka_2.13-3.8.0.tgz
cd kafka_2.13-3.8.0
```

**Start Kafka in KRaft mode** (no ZooKeeper needed, modern Kafka):

```bash
# One-time: generate a cluster ID and format storage
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t "$KAFKA_CLUSTER_ID" -c config/kraft/server.properties

# Start the broker (keep this terminal open)
bin/kafka-server-start.sh config/kraft/server.properties
```

**In a new terminal, create the topic** (from the same `kafka_2.13-3.8.0` folder):

```bash
bin/kafka-topics.sh \
  --create \
  --topic student_activities \
  --bootstrap-server localhost:9092

# Verify
bin/kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092
```

## 2. Project setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
```

Edit `.env` and replace `<db_password>` in `MONGO_URI` with the real password
for the `fatehanasrin7976_db_user` MongoDB Atlas user. `.env` is git-ignored,
so the real password never gets committed.

## 3. Run it

Terminal 1 — consumer (connects to Kafka + MongoDB, stores every event):

```bash
python consumer.py
```

Terminal 2 — producer (generates 1000 random events and sends them to Kafka):

```bash
python producer.py
```

The consumer prints each event plus a running message counter and stops
automatically ~10s after the producer finishes (idle timeout, configurable
via `CONSUMER_IDLE_TIMEOUT_MS` in `.env`).

Then, once events are stored in MongoDB:

```bash
python analytics.py       # prints totals + most active student
python visualization.py   # saves student_activity_chart.png and shows it
```

## Files

- `db.py` — shared MongoDB connection helper
- `producer.py` — Kafka producer, generates 1000 random student activity events
- `consumer.py` — Kafka consumer, stores events in MongoDB, tracks a message counter
- `analytics.py` — computes totals per activity type + most active student
- `visualization.py` — bar chart of the analytics via Matplotlib

## Notes

- No Docker anywhere — Kafka runs as a local process (KRaft mode) on your
  own machine, started with the Apache Kafka scripts above.
- MongoDB connection uses `pymongo` with the Atlas SRV connection string
  from `MONGO_URI`, read from `.env` (never hardcoded, never committed).
