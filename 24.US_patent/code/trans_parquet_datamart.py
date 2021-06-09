from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
#sc = SparkContext(conf = conf)
spark = SparkSession(sc)

path = 'D:/rawdata/'
target_month = ['202006', '202007', '202008', '202009', '202010', '202011', '202012', '202101', '202102', 'back']
file_name = ['US_BIBLIO_','US_IPC_','US_REL_PSN_']
extend_name = '.txt'
spark_read_option = spark.read.option("header", "true").option("delimiter", "��")

# read for df_us_biblo first month dataset
DF_US_BIBLIO = spark_read_option.csv(path+file_name[0]+"202005"+extend_name)
DF_US_IPC = spark_read_option.csv(path+file_name[1]+"202005"+extend_name)
DF_US_REL_PSN = spark_read_option.csv(path+file_name[2]+"202005"+extend_name)

# union anothers
for i in target_month:
    path_biblio = path+file_name[0]+i+extend_name
    path_ipc = path+file_name[1]+i+extend_name
    path_rel_psn = path+file_name[2]+i+extend_name
    DF_US_BIBLIO_temp = spark_read_option.csv(path_biblio)
    DF_US_BIBLIO = DF_US_BIBLIO.unionByName(DF_US_BIBLIO_temp)
    DF_US_IPC_temp = spark_read_option.csv(path_ipc)
    DF_US_IPC = DF_US_IPC.unionByName(DF_US_IPC_temp)
    DF_US_REL_PSN_temp = spark_read_option.csv(path_rel_psn)
    DF_US_REL_PSN = DF_US_REL_PSN.unionByName(DF_US_REL_PSN_temp)


#tree uninoned dataframe (DF_US_BIBLIO, DF_US_IPC, DF_US_REL_PSN) filter works
doc_end_2digit = F.substring(F.col("�����ȣ"), -2, 2) 

# 1) DF_US_IPC filtered and write parquet
DF_US_IPC_Filtered = \
    DF_US_IPC \
    .select("�����ȣ", "IPC�ڵ�") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .distinct()
DF_US_IPC_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_IPC_Filtered.parquet")

# 2) DF_US_BIBLIO filtered and write parquet
DF_US_BIBLIO_Filtered = \
    DF_US_BIBLIO \
    .select("�����ȣ", "�����ȣ", "������ȣ", "��Ϲ�ȣ", "�������", "�߸��Ǹ�Ī") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("�������")>=F.lit(19900101)) \
    .withColumn("�������", F.substring(F.col("�������"),1,4)) \
    .withColumn("�������", F.substring(F.col("�������"),1,6)) \
    .drop("�������") \
    .distinct()
DF_US_BIBLIO_Filtered.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_BIBLIO_Filtered.parquet")

# 3) DF_US_REL_PSN filtered and write parquet
DF_US_REL_PSN_Filtered = \
    DF_US_REL_PSN \
    .select("�����ȣ", "�̸�", "����") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("����")==F.lit("�����")) \
    .distinct()
# after 1990's  unique �����ȣ datas
DOC_1990_Filtered = \
    DF_US_BIBLIO \
    .select("�����ȣ") \
    .filter(doc_end_2digit.isin(F.lit("A1"), F.lit("B1"))) \
    .filter(F.col("�������")>=F.lit(19900101)) \
    .distinct()
# join repeatly five times for ����� 1~5
DF_US_REL_PSN_Filtered_join = \
    DOC_1990_Filtered \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", "����",F.col("�̸�").alias("�����1")).filter(F.col("�Ϸù�ȣ")==F.lit(1)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����2")).filter(F.col("�Ϸù�ȣ")==F.lit(2)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����3")).filter(F.col("�Ϸù�ȣ")==F.lit(3)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����4")).filter(F.col("�Ϸù�ȣ")==F.lit(4)), on="�����ȣ", how="left") \
    .join(DF_US_REL_PSN_Filtered.select("�����ȣ", F.col("�̸�").alias("�����5")).filter(F.col("�Ϸù�ȣ")==F.lit(5)), on="�����ȣ", how="left") \
    .distinct()
DF_US_REL_PSN_Filtered_join.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_REL_PSN_Filtered_join.parquet")


# three parquet file read to dataframe
DF_US_REL_PSN_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_REL_PSN_Filtered_join.parquet")
DF_US_BIBLIO_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_BIBLIO_Filtered.parquet")
DF_US_IPC_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_IPC_Filtered.parquet")

# make a datamart using join three dataframes and write parquet
df_rs = \
    DF_US_IPC_Filtered_read \
    .join(DF_US_REL_PSN_Filtered_read, on="�����ȣ", how="left") \
    .join(DF_US_BIBLIO_Filtered_read, on="�����ȣ", how="left")

df_rs.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_DATAMART.parquet")
