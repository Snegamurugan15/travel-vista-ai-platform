import argparse
import json
from pathlib import Path

from azure.eventhub import EventData, EventHubProducerClient


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish Travel Vista JSONL events to Azure Event Hubs."
    )
    parser.add_argument("--connection-string", required=True, help="Event Hubs namespace connection string.")
    parser.add_argument("--eventhub-name", required=True, help="Target Event Hub name.")
    parser.add_argument(
        "--input",
        default="data/streaming/visit_events.jsonl",
        help="Path to newline-delimited JSON events.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="How many events to send per Event Hubs batch.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    producer = EventHubProducerClient.from_connection_string(
        conn_str=args.connection_string,
        eventhub_name=args.eventhub_name,
    )

    sent = 0
    current_batch_count = 0
    with producer:
        batch = producer.create_batch()
        for line in lines:
            payload = json.dumps(json.loads(line))
            event = EventData(payload)
            try:
                batch.add(event)
                current_batch_count += 1
            except ValueError:
                producer.send_batch(batch)
                sent += current_batch_count
                batch = producer.create_batch()
                batch.add(event)
                current_batch_count = 1
        if current_batch_count > 0:
            producer.send_batch(batch)
            sent += current_batch_count

    print(f"Published {sent} events from {input_path}")
