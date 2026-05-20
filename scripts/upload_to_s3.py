import os
from pathlib import Path

import boto3


DATA_FILES = [
    "destinations.csv",
    "user_preferences.csv",
    "visit_counts.csv",
    "reviews.csv",
    "activity_logs.csv",
]


def main() -> None:
    bucket = os.environ["TRAVEL_VISTA_S3_BUCKET"]
    data_dir = Path(os.getenv("TRAVEL_VISTA_DATA_DIR", "data"))
    client = boto3.client("s3")

    for file_name in DATA_FILES:
        path = data_dir / file_name
        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue
        client.upload_file(str(path), bucket, file_name)
        print(f"Uploaded {path} to s3://{bucket}/{file_name}")


if __name__ == "__main__":
    main()

