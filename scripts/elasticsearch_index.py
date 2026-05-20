import os

import pandas as pd
from elasticsearch import Elasticsearch


def main() -> None:
    endpoint = os.environ["ELASTICSEARCH_URL"]
    index_name = os.getenv("TRAVEL_VISTA_INDEX", "travel-vista-destinations")
    data_path = os.getenv("TRAVEL_VISTA_DESTINATIONS_CSV", "data/destinations.csv")

    client = Elasticsearch(endpoint)
    destinations = pd.read_csv(data_path)

    for record in destinations.to_dict("records"):
        client.index(index=index_name, id=int(record["destination_id"]), document=record)
    print(f"Indexed {len(destinations)} destinations into {index_name}")


if __name__ == "__main__":
    main()

