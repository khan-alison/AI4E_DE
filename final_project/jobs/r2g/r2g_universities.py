import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from dotenv import load_dotenv

from common.r2g_executor import R2GExecutor
from reader.raw import RawCSVReader


DATE_FORMAT = "yyyy-MM-dd"


class JobExecutor(R2GExecutor):
    def __init__(self, spark, reader, cols, input_tables, target, params):
        self.spark = spark
        self.reader = reader
        self.cols = cols
        self.input_tables = input_tables
        self.target = target
        self.partition_col = "partition_date"
        self.params = params


    def execute(self):
        df = self.read_dfs()

        self.write_df_to_parquet(
            df=df,
            target_path=self.target,
            partition_column=self.partition_col,
            write_mode="overwrite",
            process_date=self.params["process_date"]
        )

    def _transform(self, df):
        pass

    def _join_data(self, df_l, df_r):
        pass


if __name__ == "__main__":
    load_dotenv()

    # Get database connection details from environment variables
    configurations = {
        "appName": "PySpark Example - MariaDB Example",
        "master": "local",
        "target_output_path": "./golden/universities",
        "cols": [
            "url",
            "university_code",
            "university_name"
        ],
        "input_tables": [
            {
                "table": "universities",
                "path": "./raw/"
            }
        ],
        "params": {
            "process_date": "2024-07-18",
            "data_date_type": "singe"
        }
    }

    spark = SparkSession.builder \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .appName(configurations["appName"]) \
        .master(configurations["master"]) \
        .getOrCreate()

    raw_reader = RawCSVReader(
        spark,
        path_to_raw=configurations["input_tables"][0]["path"],
        table_name=configurations["input_tables"][0]["table"],
    )

    job = JobExecutor(
        spark,
        reader=raw_reader,
        cols=configurations["cols"],
        input_tables=configurations["input_tables"],
        target=configurations["target_output_path"],
        params=configurations["params"]
    )
    job.execute()