# Databricks notebook source
from pyspark.sql.functions import col, current_timestamp, from_json, input_file_name
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "travel_vista")
dbutils.widgets.text("checkpoint_root", "dbfs:/tmp/travel_vista/checkpoints")
dbutils.widgets.text("event_source_mode", "eventhubs")
dbutils.widgets.text(
    "raw_events_path",
    "abfss://raw@travelvistastorage.dfs.core.windows.net/travel-vista/events",
)
dbutils.widgets.text("eventhubs_secret_scope", "travel-vista-kv")
dbutils.widgets.text("eventhubs_secret_key", "eventhub-connection-string")
dbutils.widgets.text("bronze_table", "travel_vista_bronze_events")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
checkpoint_root = dbutils.widgets.get("checkpoint_root")
event_source_mode = dbutils.widgets.get("event_source_mode")
raw_events_path = dbutils.widgets.get("raw_events_path")
eventhubs_secret_scope = dbutils.widgets.get("eventhubs_secret_scope")
eventhubs_secret_key = dbutils.widgets.get("eventhubs_secret_key")
bronze_table = dbutils.widgets.get("bronze_table")

payload_schema = StructType(
    [
        StructField("event_id", StringType(), True),
        StructField("event_ts", StringType(), True),
        StructField("destination", StringType(), True),
        StructField("region", StringType(), True),
        StructField("package_type", StringType(), True),
        StructField("transport_mode", StringType(), True),
        StructField("number_of_persons", IntegerType(), True),
        StructField("total_price", DoubleType(), True),
        StructField("booking_status", StringType(), True),
        StructField("user_id", StringType(), True),
    ]
)

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

if event_source_mode == "eventhubs":
    eventhubs_connection = dbutils.secrets.get(
        scope=eventhubs_secret_scope,
        key=eventhubs_secret_key,
    )
    encrypted_connection = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(
        eventhubs_connection
    )

    raw_stream = (
        spark.readStream.format("eventhubs")
        .option("eventhubs.connectionString", encrypted_connection)
        .load()
        .select(
            from_json(col("body").cast("string"), payload_schema).alias("event"),
            col("enqueuedTime").alias("event_hub_enqueued_at"),
        )
        .select("event.*", "event_hub_enqueued_at")
    )
    bronze_stream = raw_stream.withColumn("_ingested_at", current_timestamp())
else:
    raw_stream = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
        .schema(payload_schema)
        .load(raw_events_path)
    )
    bronze_stream = (
        raw_stream.withColumn("_ingested_at", current_timestamp())
        .withColumn("_source_file", input_file_name())
    )

(
    bronze_stream.writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", f"{checkpoint_root}/bronze")
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.{bronze_table}")
)
