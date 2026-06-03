# Azure Databricks Real-Time Design

Travel Vista now includes a concrete Azure Databricks streaming implementation.

## Target Architecture

1. Travel booking and clickstream events are published into Azure Event Hubs.
2. Event payloads are landed into Azure Data Lake Storage Gen2 in raw JSON format.
3. Azure Databricks Auto Loader ingests those files into a Bronze Delta table.
4. A Silver streaming layer standardizes timestamps, deduplicates records, and derives unit economics such as `price_per_person`.
5. Gold aggregates publish destination-level hourly KPIs and region-level daily KPIs for dashboards and downstream APIs.

## Azure Services Used

- Azure Databricks
- Azure Data Lake Storage Gen2
- Azure Event Hubs
- Azure Key Vault
- Optional Azure Data Factory or Databricks Workflows for orchestration
- Optional Power BI for KPI consumption

## Real-Time Tables

### Bronze

- `main.travel_vista.travel_vista_bronze_events`
- Raw event payloads with ingestion metadata

### Silver

- `main.travel_vista.travel_vista_silver_visits`
- Cleaned booking and visit events
- Deduplicated on `event_id`
- Includes derived `price_per_person`

### Gold

- `main.travel_vista.travel_vista_gold_destination_hourly`
- `main.travel_vista.travel_vista_gold_region_daily`

## Deployment Flow

1. Create an Azure Databricks workspace connected to your Azure subscription.
2. Create or attach an ADLS Gen2 storage account and grant the Databricks access connector permission.
3. Land event files under `abfss://raw@<storage-account>.dfs.core.windows.net/travel-vista/events`.
4. Set a Databricks cluster and configure Unity Catalog access.
5. Set bundle variables in `databricks.yml`.
6. Deploy the bundle:

```bash
databricks bundle deploy
databricks bundle run travel_vista_realtime_pipeline
```

## Notes

- The repo is safe for GitHub because it does not contain Azure secrets or workspace tokens.
- Secret values should live in Azure Key Vault and Databricks secret scopes.
- The notebooks use standard Delta and Structured Streaming patterns, so they can evolve into DLT or Lakeflow pipelines later.
