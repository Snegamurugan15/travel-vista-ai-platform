from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def platform_summary() -> dict:
    destinations = load_csv("destinations.csv")
    reviews = load_csv("reviews.csv")
    visits = load_csv("visit_counts.csv")
    logs = load_csv("activity_logs.csv")
    return {
        "destinations": len(destinations),
        "reviews": len(reviews),
        "visit_records": len(visits),
        "activity_events": len(logs),
    }


def top_destinations(limit: int = 10) -> list[dict]:
    visits = load_csv("visit_counts.csv")
    if visits.empty:
        return []
    numeric = visits.select_dtypes("number")
    if numeric.empty:
        return visits.head(limit).to_dict("records")
    score_column = numeric.columns[-1]
    return visits.sort_values(score_column, ascending=False).head(limit).to_dict("records")
