from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

DF_US_BIBLIO_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_BIBLIO.parquet")    
DF_US_REL_PSN_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_REL_PSN.parquet")    
DF_US_IPC_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_IPC.parquet")    

doc_end_2digit = F.substring(F.col("�����ȣ"), -2, 2) 
DOC_1990_Filtered = \
    DF_US_BIBLIO_read    \
    .select("�����ȣ") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("�������")>=F.lit(19900101)) \
    .distinct()

DF_US_REL_PSN_Filtered = \
    DF_US_REL_PSN_read    \
    .select("�����ȣ", "�̸�", "����") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("����")==F.lit("�����")) \
    .distinct()

DF_US_REL_PSN_Filtered_join = \
    DOC_1990_Filtered \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", "����",F.col("�̸�").alias("�����1")).filter(F.col("�Ϸù�ȣ")==F.lit(1)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����2")).filter(F.col("�Ϸù�ȣ")==F.lit(2)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����3")).filter(F.col("�Ϸù�ȣ")==F.lit(3)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����4")).filter(F.col("�Ϸù�ȣ")==F.lit(4)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����5")).filter(F.col("�Ϸù�ȣ")==F.lit(5)), on="�����ȣ", how="left") \
    .distinct()

# US_REL_PSN filtered and write to parquet
DF_US_REL_PSN_Filtered_join.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_REL_PSN_Filtered.parquet")

DF_US_IPC_Filtered = \
    DF_US_IPC_read    \
    .select("�����ȣ", "IPC�ڵ�") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .distinct() \
    .withColumn('IPC�ڵ�', F.regexp_replace('IPC�ڵ�', ' ', ''))

# US_IPC filtered and write to parquet
DF_US_IPC_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_IPC_Filtered.parquet")

DF_US_BIBLIO_Filtered = \
    DF_US_BIBLIO_read    \
    .select("�����ȣ", "�����ȣ", "������ȣ", "��Ϲ�ȣ", "�������", "�߸��Ǹ�Ī") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("�������")>=F.lit(19900101)) \
    .withColumn("�������", F.substring(F.col("�������"),1,4)) \
    .withColumn("�������", F.substring(F.col("�������"),1,6)) \
    .drop("�������") \
    .distinct()

# US_BIBLIO filtered and write to parquet
DF_US_BIBLIO_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_BIBLIO_Filtered.parquet")

