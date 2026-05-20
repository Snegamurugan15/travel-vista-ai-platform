from pathlib import Path

import pandas as pd

from src.config import MODEL_DIR


FEATURES = [
    "Age_Group",
    "Travel_Frequency",
    "Interest_in_VR",
    "Past_Experience_Rating",
    "Package_Type",
    "Duration_Days",
    "Price_USD",
]


def model_path() -> Path:
    return MODEL_DIR / "vr_engagement_model.pkl"


def predict_vr_engagement(payload: dict) -> dict:
    path = model_path()
    if not path.exists():
        return {"available": False, "message": "VR engagement model file is not available."}

    try:
        import joblib

        model = joblib.load(path)
        frame = pd.DataFrame([{feature: payload.get(feature) for feature in FEATURES}])
        prediction = int(model.predict(frame)[0])
        result = {"available": True, "prediction": prediction, "label": "Likely to engage" if prediction else "Not likely"}
        if hasattr(model, "predict_proba"):
            result["probability"] = round(float(model.predict_proba(frame)[0][1]), 4)
        return result
    except Exception as exc:
        return {"available": False, "message": str(exc)}

