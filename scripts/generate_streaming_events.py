import argparse
import csv
import json
import random
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path


BOOKING_STATUSES = ["booked", "cancelled", "pending"]
TRANSPORT_MODES = ["Flight", "Train", "Bus", "Cruise"]
PACKAGE_TYPES = ["Budget", "Standard", "Luxury", "Premium"]


def load_visit_rows(csv_path: Path) -> list[dict]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_event(row: dict, index: int, base_time: datetime) -> dict:
    travellers = max(1, int(float(row["number_of_persons"])))
    total_price = float(row["total_price"])
    region = row.get("continent", "Unknown")

    return {
        "event_id": str(uuid.uuid4()),
        "event_ts": (base_time + timedelta(minutes=index * 3)).isoformat(),
        "destination": row["destination"],
        "region": region,
        "package_type": random.choice(PACKAGE_TYPES),
        "transport_mode": random.choice(TRANSPORT_MODES),
        "number_of_persons": travellers,
        "total_price": round(total_price, 2),
        "booking_status": random.choices(BOOKING_STATUSES, weights=[0.72, 0.08, 0.20])[0],
        "user_id": f"user_{random.randint(1000, 9999)}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate newline-delimited JSON events for the Travel Vista Databricks pipeline."
    )
    parser.add_argument(
        "--input-csv",
        default="data/visit_counts.csv",
        help="Source CSV used to generate synthetic booking events.",
    )
    parser.add_argument(
        "--output",
        default="data/streaming/visit_events.jsonl",
        help="Destination JSONL file.",
    )
    parser.add_argument(
        "--events",
        type=int,
        default=250,
        help="Number of events to generate.",
    )
    args = parser.parse_args()

    rows = load_visit_rows(Path(args.input_csv))
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    base_time = datetime.now(UTC) - timedelta(hours=6)
    events: list[dict] = []
    for index in range(args.events):
        source_row = rows[index % len(rows)]
        events.append(build_event(source_row, index, base_time))

    with output_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")

    print(f"Wrote {len(events)} events to {output_path}")


if __name__ == "__main__":
    main()
