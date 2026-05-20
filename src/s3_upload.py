# s3_upload.py
import boto3, os

s3_client = boto3.client('s3')
bucket_name = 'travelvistaapp'
files_to_upload = [
    'destinations.csv', 'user_preferences.csv',
    'visit_counts.csv', 'reviews.csv', 'activity_logs.csv'
]

for file_name in files_to_upload:
    if os.path.exists(file_name):
        try:
            s3_client.upload_file(file_name, bucket_name, file_name)
            print(f"Uploaded {file_name} to bucket {bucket_name}.")
        except Exception as e:
            print(f"Error uploading {file_name}: {e}")
    else:
        print(f"File {file_name} not found.")
