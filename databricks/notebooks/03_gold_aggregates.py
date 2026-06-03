# Databricks notebook source
from pyspark.sql.functions import avg, col, count, date_trunc, sum, to_date

dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "travel_vista")
dbutils.widgets.text("checkpoint_root", "dbfs:/tmp/travel_vista/checkpoints")
dbutils.widgets.text("silver_table", "travel_vista_silver_visits")
dbutils.widgets.text("destination_table", "travel_vista_gold_destination_hourly")
dbutils.widgets.text("region_table", "travel_vista_gold_region_daily")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
checkpoint_root = dbutils.widgets.get("checkpoint_root")
silver_table = dbutils.widgets.get("silver_table")
destination_table = dbutils.widgets.get("destination_table")
region_table = dbutils.widgets.get("region_table")

silver_stream = spark.readStream.table(f"{catalog}.{schema}.{silver_table}")

destination_kpis = (
    silver_stream.withColumn("hour_bucket", date_trunc("hour", col("event_timestamp")))
    .groupBy("hour_bucket", "destination", "package_type")
    .agg(
        count("*").alias("booking_events"),
        sum("total_price").alias("gross_booking_value"),
        avg("price_per_person").alias("avg_price_per_person"),
    )
)

region_kpis = (
    silver_stream.withColumn("event_date", to_date("event_timestamp"))
    .groupBy("event_date", "region", "booking_status")
    .agg(
        count("*").alias("booking_events"),
        sum("total_price").alias("gross_booking_value"),
    )
)

(
    destination_kpis.writeStream.format("delta")
    .outputMode("complete")
    .option("checkpointLocation", f"{checkpoint_root}/gold_destination")
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.{destination_table}")
)

(
    region_kpis.writeStream.format("delta")
    .outputMode("complete")
    .option("checkpointLocation", f"{checkpoint_root}/gold_region")
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.{region_table}")
)
