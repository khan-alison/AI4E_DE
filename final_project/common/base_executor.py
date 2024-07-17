from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    def __init__(self, spark):
        self.spark = spark

    @abstractmethod
    def read_dfs(self):
        raise NotImplementedError

    @staticmethod
    def write_df_to_parquet(df, target_path, partition_column, write_mode, process_date):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError
    