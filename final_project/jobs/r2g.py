from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import functions as F
import os
from helper.multithread_helper import multithread_helper
from helper.logger_helper import LoggerSimple


logger = LoggerSimple.get_logger(__name__)

spark = SparkSession.builder.appName('ETL').config('spark.driver.memory', '4g').config(
    "spark.sql.sources.partitionOverwriteMode", "dynamic").config("spark.sql.shuffle.partitions", "12").getOrCreate()


def read_csv_file(file_path):
    try:
        df = spark.read.options(
            header=True, inferSchema=True).csv(file_path).cache()
        return df
    except Exception as e:
        logger.error(f'Failed to read {file_path}: {e}')
        return None


def normalize_exam_data(df):
    exam_fact_table = df.select('schoolYear', 'stt', 'studentCode', F.explode(F.array(
        F.struct(F.lit('TOAN').alias('subject'), F.col('TOAN').alias('score')),
        F.struct(F.lit('VAN').alias('subject'), F.col('VAN').alias('score')),
        F.struct(F.lit('LY').alias('subject'), F.col('LY').alias('score')),
        F.struct(F.lit('HOA').alias('subject'), F.col('HOA').alias('score')),
        F.struct(F.lit('SINH').alias('subject'), F.col('SINH').alias('score')),
        F.struct(F.lit('SU').alias('subject'), F.col('SU').alias('score')),
        F.struct(F.lit('DIA').alias('subject'), F.col('DIA').alias('score')),
        F.struct(F.lit('GDCD').alias('subject'), F.col('GDCD').alias('score')),
        F.struct(F.lit('NGOAINGU').alias('subject'),
                 F.col('NGOAINGU').alias('score'))
    )).alias('subject_score')).select('schoolYear', 'stt', 'studentCode', F.col('subject_score.subject'), F.col('subject_score.score'))

    dim_students = df.select('studentCode', 'schoolYear', 'stt',
                             'CODE_NGOAINGU', 'groupCode', 'groupName').distinct()

    dim_summaries = df.select('studentCode', 'schoolYear',
                              'stt', 'HKTN', 'HKXH', 'A00', 'B00', 'C00', 'D01', 'A01')

    dim_subjects = spark.createDataFrame([
        ('TOAN', 'Toán học'),
        ('VAN', 'Ngữ văn'),
        ('LY', 'Vật lý'),
        ('HOA', 'Hóa học'),
        ('SINH', 'Sinh học'),
        ('SU', 'Lịch sử'),
        ('DIA', 'Địa lý'),
        ('GDCD', 'Giáo dục công dân'),
        ('NGOAINGU', 'Ngoại ngữ')
    ], ['subject', 'description'])

    return exam_fact_table, dim_students, dim_subjects, dim_summaries


def normalize_benchmark_data(df):
    dim_majors = df.select('major_code', 'major_name').distinct()
    fact_benchmark = df.select(
        'major_code', 'subject_group', 'point', 'note', 'year')

    return dim_majors, fact_benchmark


def convert_benchmark_data_to_parquet(path):
    benchmark_years = [f'benchmark_{i}' for i in range(2019, 2024)]
    for year in benchmark_years:
        year_path = os.path.join(path, year)
        if not os.path.exists(year_path):
            logger.warning(f'Path does not exist: {year_path}')
            continue

        all_files = [os.path.join(year_path, file) for file in os.listdir(
            year_path) if file.endswith('.csv')]
        for file in all_files:
            df = read_csv_file(file)
            if df is not None:
                dim_majors, fact_benchmark = normalize_benchmark_data(
                    df)
                dim_majors, fact_benchmarks = normalize_benchmark_data(df)
            dim_majors.write.mode('overwrite').parquet(
                f'./golden/benchmark/{year}/dim_majors')
            fact_benchmarks.write.mode('overwrite').parquet(
                f'./golden/benchmark/{year}/fact_benchmarks')


def convert_universities_data_to_parquet(path):
    df = read_csv_file(path)
    df.write.parquet('./golden/universities')


def convert_exam_result_to_parquet(path):
    all_files = [os.path.join(path, file)
                 for file in os.listdir(path) if file.endswith('.csv')]
    for file in all_files:
        df = read_csv_file(file)

        if df is not None:
            exam_fact_table, dim_students, dim_subjects, dim_summaries = normalize_exam_data(
                df)
            exam_fact_table.write.mode('overwrite').parquet(
                './golden/exam_result/exam_fact_scores')
            dim_students.write.mode('overwrite').parquet(
                './golden/exam_result/dim_students')
            dim_subjects.write.mode('overwrite').parquet(
                './golden/exam_result/dim_subjects')
            dim_summaries.write.mode('overwrite').parquet(
                './golden/exam_result/dim_summaries')


if __name__ == '__main__':
    base_path = './output_data/benchmark'
    convert_benchmark_data_to_parquet(base_path)
    # universities_base_path = './output_data/universities'
    # convert_universities_data_to_parquet(universities_base_path)
    # exam_result_path = './output_data/exam_result'
    # convert_exam_result_to_parquet(exam_result_path)
