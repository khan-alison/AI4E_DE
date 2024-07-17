from common.base_executor import BaseExecutor
from reader.raw import RawCSVReader
from pyspark.sql import functions as F


class R2GExecutor(BaseExecutor):
    def __init__(self, spark, reader, input_tables, target):
        self.spark = spark
        self.reader = reader
        self.input_tables = input_tables
        self.target = target
        self.partition_col = "partition_date"

    def read_dfs(self):
        return self.reader.read_table()

    @staticmethod
    def write_df_to_parquet(df, target_path, partition_column, write_mode, process_date):
        df = df.withColumn(partition_column, F.lit(process_date))
        df.show()
        if df.count() > 0:
            df.write.partitionBy(partition_column).mode(write_mode).parquet(target_path)

    def execute(self):
        raise NotImplementedError
    