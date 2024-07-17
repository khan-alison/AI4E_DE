from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName('Raw2Insight').getOrCreate()

fact_benchmark_2019_df = spark.read.parquet('./golden/benchmark/benchmark_2019/fact_benchmarks')
dim_majors_2019_df = spark.read.parquet('./golden/benchmark/benchmark_2019/dim_majors')
fact_benchmark_2020_df = spark.read.parquet('./golden/benchmark/benchmark_2020/fact_benchmarks')
dim_majors_2020_df = spark.read.parquet('./golden/benchmark/benchmark_2020/dim_majors')
fact_benchmark_2021_df = spark.read.parquet('./golden/benchmark/benchmark_2021/fact_benchmarks')
dim_majors_2021_df = spark.read.parquet('./golden/benchmark/benchmark_2021/dim_majors')
fact_benchmark_2022_df = spark.read.parquet('./golden/benchmark/benchmark_2022/fact_benchmarks')
dim_majors_2022_df = spark.read.parquet('./golden/benchmark/benchmark_2022/dim_majors')
fact_benchmark_2023_df = spark.read.parquet('./golden/benchmark/benchmark_2023/fact_benchmarks')
dim_majors_2023_df = spark.read.parquet('./golden/benchmark/benchmark_2023/dim_majors')

fact_exam_result_df = spark.read.parquet(
    './golden/exam_result/exam_fact_scores')
dim_subjects_df = spark.read.parquet('./golden/exam_result/dim_subjects')
dim_students_df = spark.read.parquet('./golden/exam_result/dim_students')
dim_summaries_df = spark.read.parquet('./golden/exam_result/dim_summaries')

universities_df = spark.read.parquet('./golden/universities')


fact_benchmark_2023_df.show(5)



