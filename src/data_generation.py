import boto3
import pandas as pd
import io
from sklearn.preprocessing import MinMaxScaler

# AWS S3 Configuration
s3_client = boto3.client("s3")
bucket_name = "travelvistaapp"

def load_s3_csv(file_key):
    """Loads a CSV file from S3 into a Pandas DataFrame."""
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        return pd.read_csv(io.BytesIO(response["Body"].read()))
    except s3_client.exceptions.NoSuchKey:
        print(f"⚠️ Warning: '{file_key}' not found in S3 bucket '{bucket_name}'. Skipping.")
        return None
    except Exception as e:
        print(f"❌ Error loading '{file_key}': {e}")
        return None

# Load visit counts dataset
visit_counts = load_s3_csv("visit_counts.csv")

# ✅ Process Visit Counts Dataset
if visit_counts is not None:
    print("📌 Columns in visit_counts dataset:", visit_counts.columns)  # Debugging step

    # Find a valid column for normalization
    possible_columns = ["visit_count", "number_of_persons", "total_price"]
    selected_column = next((col for col in possible_columns if col in visit_counts.columns), None)

    if selected_column:
        print(f"✅ Using '{selected_column}' for normalization.")
        
        # Normalize the selected column
        scaler = MinMaxScaler()
        visit_counts["normalized_visits"] = scaler.fit_transform(visit_counts[[selected_column]])

        # Convert processed DataFrame to CSV and upload back to S3
        processed_csv = io.StringIO()
        visit_counts.to_csv(processed_csv, index=False)

        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key="processed_visit_counts.csv",
            Body=processed_csv.getvalue()
        )
        print(f"✅ Processed visit counts uploaded to S3 using column '{selected_column}'.")
    else:
        print("❌ No valid column found for normalization. Skipping visit counts processing.")
else:
    print("⚠️ Skipping visit counts processing: visit_counts.csv not found.")

print("🎉 Preprocessing completed successfully!")
