from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data_access import load_table


def _text_features(row) -> str:
    tags = row.get("dynamic_tags", [])
    modes = row.get("transport_modes", [])
    if isinstance(tags, list):
        tags_text = " ".join(map(str, tags))
    else:
        tags_text = str(tags)
    if isinstance(modes, list):
        modes_text = " ".join(map(str, modes))
    else:
        modes_text = str(modes)
    return " ".join(
        [
            str(row.get("name", "")),
            str(row.get("world_wonder", "")),
            str(row.get("package_option", "")),
            tags_text,
            modes_text,
        ]
    )


def recommend_destinations(query: str, budget: float | None = None, limit: int = 5) -> list[dict]:
    destinations = load_table("destinations").copy()
    if destinations.empty:
        return []

    if budget is not None:
        filtered = destinations[destinations["base_price"] <= float(budget)]
        if not filtered.empty:
            destinations = filtered

    documents = destinations.apply(_text_features, axis=1).tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()

    destinations["match_score"] = scores
    output_columns = [
        "destination_id",
        "name",
        "world_wonder",
        "package_option",
        "base_price",
        "discount_percentage",
        "transport_modes",
        "dynamic_tags",
        "match_score",
    ]
    return (
        destinations.sort_values(["match_score", "discount_percentage"], ascending=[False, False])
        .head(limit)[output_columns]
        .round({"base_price": 2, "match_score": 3})
        .to_dict("records")
    )

