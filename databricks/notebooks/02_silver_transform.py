# Databricks notebook source
from pyspark.sql.functions import col, current_timestamp, expr, to_timestamp

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "travel_vista")
dbutils.widgets.text("checkpoint_root", "dbfs:/tmp/travel_vista/checkpoints")
dbutils.widgets.text("bronze_table", "travel_vista_bronze_events")
dbutils.widgets.text("silver_table", "travel_vista_silver_visits")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
checkpoint_root = dbutils.widgets.get("checkpoint_root")
bronze_table = dbutils.widgets.get("bronze_table")
silver_table = dbutils.widgets.get("silver_table")

bronze_stream = spark.readStream.table(f"{catalog}.{schema}.{bronze_table}")

silver_stream = (
    bronze_stream.filter(col("event_id").isNotNull())
    .withColumn("event_timestamp", to_timestamp("event_ts"))
    .withColumn(
        "price_per_person",
        expr(
            "CASE WHEN number_of_persons IS NULL OR number_of_persons = 0 "
            "THEN NULL ELSE total_price / number_of_persons END"
        ),
    )
    .withColumn("processed_at", current_timestamp())
    .dropDuplicates(["event_id"])
)

(
    silver_stream.writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", f"{checkpoint_root}/silver")
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.{silver_table}")
)
