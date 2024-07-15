from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('ETL').getOrCreate()

df = spark.read.parquet('/Users/khanhnn/Desktop/benchmark_ANS_2019')

rs = df.where(df.subject_group == 'A00')


rs.show(20)
rs.printSchema()
# df.show()
# df.printSchema()