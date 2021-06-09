from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

DF_US_BIBLIO_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_BIBLIO.parquet")    
DF_US_REL_PSN_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_REL_PSN.parquet")    
DF_US_IPC_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_IPC.parquet")    

doc_end_2digit = F.substring(F.col("문헌번호"), -2, 2) 
DOC_1990_Filtered = \
    DF_US_BIBLIO_read    \
    .select("문헌번호") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("출원일자")>=F.lit(19900101)) \
    .distinct()

DF_US_REL_PSN_Filtered = \
    DF_US_REL_PSN_read    \
    .select("문헌번호", "이름", "국적") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("구분")==F.lit("출원인")) \
    .distinct()

DF_US_REL_PSN_Filtered_join = \
    DOC_1990_Filtered \
    .join(DF_US_REL_PSN_Filtered.select("문헌번호", "국적",F.col("이름").alias("출원인1")).filter(F.col("일련번호")==F.lit(1)), on="문헌번호", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("문헌번호", F.col("이름").alias("출원인2")).filter(F.col("일련번호")==F.lit(2)), on="문헌번호", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("문헌번호", F.col("이름").alias("출원인3")).filter(F.col("일련번호")==F.lit(3)), on="문헌번호", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("문헌번호", F.col("이름").alias("출원인4")).filter(F.col("일련번호")==F.lit(4)), on="문헌번호", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("문헌번호", F.col("이름").alias("출원인5")).filter(F.col("일련번호")==F.lit(5)), on="문헌번호", how="left") \
    .distinct()

# US_REL_PSN filtered and write to parquet
DF_US_REL_PSN_Filtered_join.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_REL_PSN_Filtered.parquet")

DF_US_IPC_Filtered = \
    DF_US_IPC_read    \
    .select("문헌번호", "IPC코드") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .distinct() \
    .withColumn('IPC코드', F.regexp_replace('IPC코드', ' ', ''))

# US_IPC filtered and write to parquet
DF_US_IPC_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_IPC_Filtered.parquet")

DF_US_BIBLIO_Filtered = \
    DF_US_BIBLIO_read    \
    .select("문헌번호", "출원번호", "공개번호", "등록번호", "출원일자", "발명의명칭") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("출원일자")>=F.lit(19900101)) \
    .withColumn("출원연도", F.substring(F.col("출원일자"),1,4)) \
    .withColumn("출원연월", F.substring(F.col("출원일자"),1,6)) \
    .drop("출원일자") \
    .distinct()

# US_BIBLIO filtered and write to parquet
DF_US_BIBLIO_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_BIBLIO_Filtered.parquet")

