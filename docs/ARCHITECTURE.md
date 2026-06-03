# Architecture

Travel Vista is now structured as a real-time Azure + Databricks portfolio project, while keeping the Flask application as a lightweight analytics and recommendation surface.

## Main Layers

1. Experience layer
   - Flask dashboard at `/`
   - JSON APIs for summary metrics, destination ranking, recommendations, secure insert simulation, and VR engagement scoring

2. Streaming ingestion layer
   - Azure Event Hubs receives booking and activity events
   - Azure Data Lake Storage Gen2 stores raw landed JSON when file-based ingestion is used
   - Azure Databricks Bronze notebook ingests events into Delta Lake

3. Curated analytics layer
   - Silver streaming transformations clean timestamps, deduplicate events, and derive commercial metrics such as `price_per_person`
   - Gold streaming tables aggregate destination and regional KPIs for downstream dashboards

4. Intelligence layer
   - Recommendation engine uses TF-IDF text vectors over destinations, world wonders, package options, transport modes, and dynamic tags
   - VR engagement scoring uses the preserved model artifact from the original capstone

5. Security and operations layer
   - AES encryption demo for sensitive payloads
   - Azure Key Vault and Databricks secret scopes are the intended secret-management pattern
   - Databricks Asset Bundle config defines the deployable job workflow

## Azure + Databricks Assets In Repo

- `databricks.yml`
- `databricks/notebooks/01_bronze_ingest.py`
- `databricks/notebooks/02_silver_transform.py`
- `databricks/notebooks/03_gold_aggregates.py`
- `docs/AZURE_DATABRICKS_REALTIME.md`
- `scripts/generate_streaming_events.py`
- `scripts/publish_events_to_event_hub.py`

## Original WIL Source Used

The cleaned repository was rebuilt from:

- `TRAVEL VISTA - MID TERM - WEEK 6/Codes`
- `Week 6 deliverables/travel_insights_dashboard`
- `Week 12 deliverables`
- `TRAVEL VISTA - MID TERM - WEEK 6/Mid_Term_Presentation.pptx`

Local virtual environments, personal career documents, videos, and hardcoded secrets were intentionally excluded.

