# Travel Vista Azure Databricks Real-Time Platform

Travel Vista is now structured as a real-time Azure data engineering project built around Azure Databricks, Delta Lake, Azure Event Hubs, and Azure Data Lake Storage Gen2. It keeps the original Flask analytics app and recommendation layer, but the main portfolio signal is now a deployable streaming architecture rather than a standalone local Spark script.

## What This Project Shows

- Real-time ingestion with Azure Event Hubs
- Azure Databricks Structured Streaming notebooks
- Bronze, Silver, and Gold Delta Lake design
- Azure Data Lake Storage Gen2 integration
- Databricks Asset Bundle job orchestration
- Event generation and Event Hubs publishing utilities
- Flask API and dashboard for analytics consumption
- Recommendation logic and VR model integration from the original capstone

## Target Architecture

```text
Travel events -> Azure Event Hubs -> Azure Databricks -> Delta Lake (Bronze/Silver/Gold)
                                           |                    |
                                           v                    v
                                ADLS Gen2 raw landing      Flask analytics / BI
```

### Streaming Flow

1. Booking and travel activity events are published to Azure Event Hubs.
2. Azure Databricks ingests the stream into a Bronze Delta table.
3. Silver transformations standardize timestamps, deduplicate records, and derive business metrics like `price_per_person`.
4. Gold tables produce destination-level hourly KPIs and region-level daily KPIs.
5. The Flask app and downstream dashboards can consume curated outputs.

## Repository Structure

```text
travel-vista-ai-platform/
  app.py                                      # Flask dashboard and APIs
  data/                                       # Synthetic source CSVs
  databricks.yml                              # Databricks Asset Bundle
  databricks/
    README.md                                 # Databricks deployment notes
    notebooks/
      01_bronze_ingest.py                     # Event Hubs / ADLS -> Bronze Delta
      02_silver_transform.py                  # Bronze -> Silver Delta
      03_gold_aggregates.py                   # Silver -> Gold Delta
  docs/
    ARCHITECTURE.md                           # Repo architecture
    AZURE_DATABRICKS_REALTIME.md              # Azure deployment design
  scripts/
    generate_streaming_events.py              # Create JSONL event stream
    publish_events_to_event_hub.py            # Push events to Azure Event Hubs
    load_to_postgres_async.py                 # Existing async loader
    elasticsearch_index.py                    # Existing search indexing utility
  src/                                        # Analytics, recommender, security, VR logic
```

## Azure Databricks Deployment

### Prerequisites

- Azure subscription
- Azure Databricks workspace
- Azure Event Hubs namespace + event hub
- Azure Data Lake Storage Gen2 account + container
- Unity Catalog-enabled cluster or assigned workspace catalog/schema
- Databricks CLI configured locally

### Bundle Variables

The Databricks workflow is configured in `databricks.yml`. Set:

- `databricks_host`
- `cluster_id`
- `catalog`
- `schema`
- `checkpoint_root`
- `event_source_mode`
- `raw_events_path`
- `eventhubs_secret_scope`
- `eventhubs_secret_key`

### Deploy

```bash
databricks bundle deploy
databricks bundle run travel_vista_realtime_pipeline
```

## Generate and Publish Test Events

Generate synthetic booking events from the existing Travel Vista dataset:

```powershell
python scripts/generate_streaming_events.py --events 250
```

Publish them into Azure Event Hubs:

```powershell
python scripts/publish_events_to_event_hub.py `
  --connection-string "Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<policy>;SharedAccessKey=<key>" `
  --eventhub-name "travel-vista-events"
```

## Local App

The Flask app is still available for local demonstration:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Optional Dependencies

For the Databricks and streaming tooling:

```powershell
pip install -r requirements-optional.txt
```

## Notes

- This repository is safe to publish because it does not include Azure secrets, tokens, or workspace-specific IDs.
- Azure secrets should be stored in Key Vault and exposed to Databricks through secret scopes.
- The original WIL capstone assets remain the source for the Flask, recommendation, and VR pieces, but the data engineering side is now framed as a real Azure Databricks streaming project.
