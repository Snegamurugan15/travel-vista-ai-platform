# Travel Vista AI Platform

Travel Vista is a WIL capstone project for a secure AI-powered travel platform. The original project combined a Flask backend, cloud-storage concepts, PostgreSQL/MongoDB persistence, Kafka/Spark-style data processing, and security features such as TLS, OAuth, and AES/RSA-style encryption.

This cleaned portfolio version keeps the project as a Flask/API platform rather than converting it into a Streamlit dashboard. It removes the hardcoded OAuth secrets from the original prototype and keeps safe CSV extracts for local analytics.

## What This Demonstrates

- Flask API design for travel-platform services.
- AES encryption utility for sensitive payload handling.
- Analytics endpoints over destination, review, visit, and activity-log data.
- Separation between API code and data-processing utilities.
- Cloud architecture thinking around S3, relational storage, and scalable processing.

## Repository Structure

- `app.py` - cleaned Flask API and browser landing page.
- `src/analytics.py` - reusable data-loading and summary logic.
- `src/data_generation.py`, `src/s3_upload.py`, `src/rds_insert.py` - selected original support scripts.
- `data/*.csv` - safe project CSV extracts.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## API Examples

```powershell
curl http://127.0.0.1:5000/api/summary
curl http://127.0.0.1:5000/api/top-destinations?limit=5
```

```powershell
curl -X POST http://127.0.0.1:5000/api/secure-insert `
  -H "Content-Type: application/json" `
  -d "{\"sensitive_field\":\"passport-like-demo-value\"}"
```

## Security Note

The original client ID, client secret, and static encryption values were removed from the public project. Use environment variables such as `FLASK_SECRET_KEY` and `TRAVEL_VISTA_AES_KEY` for real deployments.
