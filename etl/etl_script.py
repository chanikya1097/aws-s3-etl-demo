import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from pyspark.sql.functions import col, trim

# Glue boilerplate
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Common S3 paths
input_base = "s3://aws-s3-etl-demo1/data/"
output_base = "s3://aws-s3-etl-demo1/cleaned/"

# Helper to clean and write CSV
def clean_and_write(file_name):
    print(f"Processing {file_name}...")
    df = spark.read.option("header", True).csv(f"{input_base}{file_name}")

    # Remove rows with nulls in all columns
    df = df.dropna(how="all")

    # Trim whitespace from all string columns
    for column in df.columns:
        df = df.withColumn(column, trim(col(column)))

    # Write cleaned data
    df.write.mode("overwrite").csv(f"{output_base}{file_name.replace('.csv', '')}/", header=True)

# List of files to clean
csv_files = ["account.csv", "customer.csv", "financial_data_updated.csv", "transaction.csv"]

for file in csv_files:
    clean_and_write(file)

job.commit()
