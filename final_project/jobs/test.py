from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import functions as F
import os
from helper.multithread_helper import multithread_helper
from helper.logger_helper import LoggerSimple

logger = LoggerSimple.get_logger(__name__)

spark = SparkSession.builder.appName('ETL').config('spark.driver.memory', '4g').config(
    "spark.sql.sources.partitionOverwriteMode", "dynamic").config("spark.sql.shuffle.partitions", "1000").getOrCreate()


# Function to read CSV files using Spark
def read_csv_file(file_path):
    try:
        df = spark.read.options(header=True, inferSchema=True).csv(file_path).cache()
        return df
    except Exception as e:
        logger.error(f'Failed to read {file_path}: {e}')
        return None


# Path to the benchmark folders
base_path = '/Users/khanhnn/Developer/DE/AI4E_DE_05/final_project/output_data/benchmark'

# Get list of benchmark years
benchmark_years = [f'benchmark_{i}' for i in range(2019, 2024)]

# Get all CSV files from the benchmark folders
all_files = [os.path.join(base_path, year, file) for year in benchmark_years for file in
             os.listdir(os.path.join(base_path, year)) if file.endswith('.csv')]

# Use the multithread_helper to read all CSV files concurrently
df_list = multithread_helper(items=all_files, method=read_csv_file, max_workers=12)

# Filter out any None values in the df_list
df_list = [df for df in df_list if df is not None]

# Concatenate all DataFrames into one using union operation
df = df_list[0]
for df_part in df_list[1:]:
    df = df.union(df_part)

# Perform any additional transformations if needed (uncomment and modify if needed)
# df = df.withColumn('zone', F.substring(df['note'], -1, 1))

# Write the final DataFrame to Parquet
df.write.format('parquet').mode('overwrite').save(
    '/Users/khanhnn/Developer/DE/AI4E_DE_05/final_project/golden/benchmark_all_years')

# Stop the Spark session
spark.stop()
