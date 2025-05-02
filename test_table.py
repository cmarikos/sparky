from pyspark.sql import SparkSession 

# ─── 1) Bootstrap Spark ────────────────────────────────────────────────
spark = SparkSession.builder \
    .appName("TestBigQueryReadWrite") \
    .getOrCreate()

# ─── 2) Read from BigQuery ────────────────────────────────────────────
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("/Users/cmarikos/Downloads/RAZE VR voterfile match - results-20250402-095044 (1).csv")
df.show(5)

# ─── 3) Write back to BigQuery ────────────────────────────────────────
df.write.format("bigquery") \
  .option("table", "prod-organize-arizon-4e1c0a83:sparky.test_table") \
  .mode("overwrite") \
  .save()


# ─── 4) Clean up ───────────────────────────────────────────────────────
spark.stop()