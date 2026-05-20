"""Generate local Travel Vista demo data.

The WIL project already includes generated CSVs under data/. This script keeps
the generation workflow reproducible for future portfolio improvements.
"""

from pathlib import Path
import random

import pandas as pd


OUTPUT_DIR = Path("data")
WONDERS = [
    "Great Wall of China",
    "Petra",
    "Christ the Redeemer",
    "Machu Picchu",
    "Chichen Itza",
    "Roman Colosseum",
    "Taj Mahal",
]
TAGS = ["cultural", "scenic", "family", "luxury", "budget", "adventurous"]
TRANSPORT = ["flight", "train", "cruise"]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    destinations = []
    for destination_id in range(1, 29):
        wonder = WONDERS[(destination_id - 1) % len(WONDERS)]
        option = random.choice(["wonder_only", "surroundings", "premium_bundle", "vr_preview"])
        destinations.append(
            {
                "destination_id": destination_id,
                "name": f"{wonder} - {option}",
                "world_wonder": wonder,
                "package_option": option,
                "base_price": round(random.uniform(900, 5000), 2),
                "discount_percentage": random.choice([0, 5, 10, 15, 20]),
                "transport_modes": random.sample(TRANSPORT, random.randint(1, 3)),
                "dynamic_tags": random.sample(TAGS, random.randint(2, 4)),
                "created_at": pd.Timestamp.now().isoformat(),
            }
        )
    pd.DataFrame(destinations).to_csv(OUTPUT_DIR / "destinations.csv", index=False)

    visits = []
    for visit_id in range(1, 501):
        visits.append(
            {
                "visit_id": visit_id,
                "user_id": random.randint(1, 250),
                "destination_id": random.randint(1, 28),
                "visit_timestamp": pd.Timestamp.now() - pd.Timedelta(days=random.randint(0, 730)),
                "region": random.choice(["North America", "Europe", "Asia", "South America"]),
                "number_of_persons": random.randint(1, 6),
                "total_price": round(random.uniform(500, 20000), 2),
            }
        )
    pd.DataFrame(visits).to_csv(OUTPUT_DIR / "visit_counts.csv", index=False)

    print("Generated destinations.csv and visit_counts.csv")


if __name__ == "__main__":
    main()

