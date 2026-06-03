# Travel Vista AI Platform

Travel Vista is a WIL capstone portfolio project for a secure AI-powered travel platform. The project combines travel package analytics, recommendation logic, cloud data-pipeline scripts, and a VR engagement model into one clean public repository.

The current repo is rebuilt from the local WIL project folder and keeps the project as a Flask/API and data-engineering application rather than turning everything into a Streamlit demo.

## Project Highlights

- Flask dashboard and JSON API for travel analytics
- Destination recommendation engine using TF-IDF and cosine similarity
- AES encryption demo for sensitive travel-platform payloads
- CSV-backed analytics over destinations, reviews, activity logs, preferences, and visit records
- VR engagement model asset from the Week 12 deliverable
- Sanitized AWS S3, PostgreSQL, PySpark, Databricks-ready ETL, and Elasticsearch scripts
- Midterm presentation included under `docs/`

## Repository Structure

```text
travel-vista-ai-platform/
  app.py                         # Main Flask dashboard and API
  data/                          # Synthetic WIL project CSV extracts
  docs/                          # Architecture notes and presentation
  models/                        # VR engagement model artifact
  scripts/                       # Cloud/data engineering scripts
  src/                           # Analytics, recommender, security, model utilities
  legacy/                        # Notes about original deliverables
```

## Main App

Run the local Flask app:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## API Examples

```powershell
curl http://127.0.0.1:5000/api/summary
curl http://127.0.0.1:5000/api/destinations
curl "http://127.0.0.1:5000/api/recommend?query=scenic luxury family flight&budget=3500"
```

```powershell
curl -X POST http://127.0.0.1:5000/api/secure-insert `
  -H "Content-Type: application/json" `
  -d "{\"sensitive_field\":\"passport-demo-value\"}"
```

VR engagement prediction:

```powershell
curl -X POST http://127.0.0.1:5000/api/vr-engagement `
  -H "Content-Type: application/json" `
  -d "{\"Age_Group\":\"26-35\",\"Travel_Frequency\":\"Frequently\",\"Interest_in_VR\":5,\"Past_Experience_Rating\":8,\"Package_Type\":\"Premium\",\"Duration_Days\":9,\"Price_USD\":2400}"
```

## Data Engineering Scripts

The repo includes production-style scripts, but they require environment variables before use:

```powershell
$env:TRAVEL_VISTA_S3_BUCKET="your-bucket"
python scripts/upload_to_s3.py
```

```powershell
$env:DATABASE_URL="postgresql+asyncpg://user:password@host:5432/dbname"
$env:TRAVEL_VISTA_AES_KEY="replace-with-16-byte-key"
python scripts/load_to_postgres_async.py
```

Optional infrastructure scripts:

```powershell
python scripts/pyspark_pipeline.py
python scripts/elasticsearch_index.py
```

The Spark pipeline uses standard `SparkSession` APIs and Parquet output, so it can be adapted to Azure Databricks jobs or notebooks with environment-specific path changes.

## Source Notes

This public repo was rebuilt from the WIL source folders:

- `TRAVEL VISTA - MID TERM - WEEK 6/Codes`
- `Week 6 deliverables/travel_insights_dashboard`
- `Week 12 deliverables`

Personal career documents, local virtual environments, videos, and hardcoded credentials were excluded. The original midterm Flask app included secrets, so its behavior was recreated in sanitized code instead of publishing the raw file.

## Portfolio Positioning

Use this as a cloud/data/AI platform project on a resume. It shows API design, analytics engineering, ML model integration, recommendation systems, secure configuration practices, and cloud pipeline awareness, with PySpark patterns that translate cleanly to Databricks-based data engineering workflows.
