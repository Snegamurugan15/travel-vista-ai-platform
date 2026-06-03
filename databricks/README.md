# Azure Databricks Deployment

This folder contains the real-time Azure Databricks implementation for Travel Vista.

## Components

- `notebooks/01_bronze_ingest.py`
  Ingests event JSON from Azure Event Hubs or ADLS Gen2 landing files and writes a Bronze Delta table.
- `notebooks/02_silver_transform.py`
  Cleans and enriches streaming events into a Silver Delta table.
- `notebooks/03_gold_aggregates.py`
  Produces hourly destination KPIs and daily regional KPIs as Gold Delta tables.
- `bundle/`
  Reserved for optional future resource expansion.

## Azure Services

- Azure Data Lake Storage Gen2 for raw event landing and checkpoints
- Azure Databricks for Structured Streaming, Delta Lake, and job orchestration
- Azure Event Hubs as the primary event ingestion source
- Azure Key Vault for secrets referenced by Databricks secret scopes

## Expected Event Shape

The pipeline expects newline-delimited JSON events with fields such as:

- `event_id`
- `event_ts`
- `destination`
- `region`
- `package_type`
- `transport_mode`
- `number_of_persons`
- `total_price`
- `booking_status`
- `user_id`

Sample events can be generated locally with `scripts/generate_streaming_events.py`.
