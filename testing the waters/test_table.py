from pyspark.sql import SparkSession
from pyspark import SparkFiles

# 1) Bootstrap Spark (now SparkFiles._sc is set)
spark = SparkSession.builder \
    .appName("TestBigQueryReadWrite") \
    .getOrCreate()

# 2) Grab the local path to the shipped credentials
cred_path = SparkFiles.get("spark-bigquery-sa.json")

# 3) Read your CSV
df = spark.read.csv(
    "/Users/cmarikos/Downloads/RAZE VR voterfile match - results-20250402-095044 (1).csv",
    header=True, inferSchema=True
)
df.show(5)

# 4) Write back to BigQuery
df.write \
  .format("bigquery") \
  .option("table", "prod-organize-arizon-4e1c0a83.sparky.test_table") \
  .option("writeMethod", "direct") \
  .option("credentialsFile", cred_path) \
  .option("writeDisposition", "WRITE_TRUNCATE") \
  .save()


spark.stop()
