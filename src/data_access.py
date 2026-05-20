import ast
import json
from functools import lru_cache

import pandas as pd

from src.config import CSV_FILES, DATA_DIR


def _parse_json_like(value):
    if pd.isna(value) or value == "":
        return []
    if isinstance(value, (list, dict)):
        return value
    text = str(value)
    for parser in (json.loads, ast.literal_eval):
        try:
            return parser(text)
        except Exception:
            continue
    return text


@lru_cache(maxsize=16)
def load_table(name: str) -> pd.DataFrame:
    if name not in CSV_FILES:
        raise KeyError(f"Unknown table: {name}")
    path = DATA_DIR / CSV_FILES[name]
    if not path.exists():
        return pd.DataFrame()

    frame = pd.read_csv(path)
    for column in ("transport_modes", "dynamic_tags", "preferences", "additional_data"):
        if column in frame.columns:
            frame[column] = frame[column].apply(_parse_json_like)
    for column in ("created_at", "review_timestamp", "visit_timestamp", "activity_timestamp", "last_updated"):
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")
    return frame


def all_tables() -> dict[str, pd.DataFrame]:
    return {name: load_table(name) for name in CSV_FILES}

