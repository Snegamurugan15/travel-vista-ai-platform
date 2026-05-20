from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("TRAVEL_VISTA_DATA_DIR", BASE_DIR / "data"))
MODEL_DIR = Path(os.getenv("TRAVEL_VISTA_MODEL_DIR", BASE_DIR / "models"))

CSV_FILES = {
    "destinations": "destinations.csv",
    "reviews": "reviews.csv",
    "visits": "visit_counts.csv",
    "preferences": "user_preferences.csv",
    "activity_logs": "activity_logs.csv",
}

