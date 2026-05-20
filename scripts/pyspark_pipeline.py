import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def main() -> None:
    data_dir = os.getenv("TRAVEL_VISTA_DATA_DIR", "data")
    output_dir = os.getenv("TRAVEL_VISTA_OUTPUT_DIR", "outputs/processed_visits")

    spark = SparkSession.builder.appName("TravelVistaVisitPipeline").getOrCreate()
    visits = spark.read.csv(f"{data_dir}/visit_counts.csv", header=True, inferSchema=True)
    processed = visits.withColumn("price_per_person", col("total_price") / col("number_of_persons"))
    processed.write.mode("overwrite").parquet(output_dir)
    spark.stop()
    print(f"Processed visit data written to {output_dir}")


if __name__ == "__main__":
    main()

