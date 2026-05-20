import pandas as pd

from src.data_access import load_table


def platform_summary() -> dict:
    destinations = load_table("destinations")
    reviews = load_table("reviews")
    visits = load_table("visits")
    logs = load_table("activity_logs")

    return {
        "destinations": int(len(destinations)),
        "world_wonders": int(destinations["world_wonder"].nunique()) if not destinations.empty else 0,
        "reviews": int(len(reviews)),
        "average_rating": round(float(reviews["rating"].mean()), 2) if not reviews.empty else 0,
        "visit_records": int(len(visits)),
        "estimated_revenue": round(float(visits["total_price"].sum()), 2) if not visits.empty else 0,
        "activity_events": int(len(logs)),
        "active_users": int(logs["user_id"].nunique()) if not logs.empty else 0,
    }


def destination_performance(limit: int = 12) -> list[dict]:
    destinations = load_table("destinations")
    visits = load_table("visits")
    reviews = load_table("reviews")
    if destinations.empty:
        return []

    visit_metrics = pd.DataFrame()
    if not visits.empty:
        visit_metrics = (
            visits.groupby("destination_id", as_index=False)
            .agg(visits=("visit_id", "count"), revenue=("total_price", "sum"), travelers=("number_of_persons", "sum"))
        )

    review_metrics = pd.DataFrame()
    if not reviews.empty:
        review_metrics = reviews.groupby("destination_id", as_index=False).agg(
            average_rating=("rating", "mean"),
            review_count=("review_id", "count"),
        )

    frame = destinations.merge(visit_metrics, on="destination_id", how="left").merge(
        review_metrics, on="destination_id", how="left"
    )
    for column in ("visits", "revenue", "travelers", "average_rating", "review_count"):
        frame[column] = frame[column].fillna(0)

    frame["score"] = (
        frame["visits"].rank(pct=True)
        + frame["revenue"].rank(pct=True)
        + frame["average_rating"].rank(pct=True)
        + (100 - frame["discount_percentage"]).rank(pct=True) / 2
    )
    return (
        frame.sort_values("score", ascending=False)
        .head(limit)
        .round({"revenue": 2, "average_rating": 2, "score": 3})
        .to_dict("records")
    )


def activity_mix() -> list[dict]:
    logs = load_table("activity_logs")
    if logs.empty:
        return []
    counts = logs["activity_type"].value_counts().reset_index()
    counts.columns = ["activity_type", "events"]
    return counts.to_dict("records")


def region_revenue() -> list[dict]:
    visits = load_table("visits")
    if visits.empty:
        return []
    frame = (
        visits.groupby("region", as_index=False)
        .agg(revenue=("total_price", "sum"), travelers=("number_of_persons", "sum"), visits=("visit_id", "count"))
        .sort_values("revenue", ascending=False)
    )
    return frame.round({"revenue": 2}).to_dict("records")

