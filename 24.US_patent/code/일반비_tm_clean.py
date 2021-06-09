from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

path = 'D:/rawdata/'
target_month = ['202006', '202007', '202008', '202009', '202010', '202011', '202012', '202101', '202102', 'back']
file_name = ['US_BIBLIO_','US_IPC_','US_REL_PSN_']
extend_name = '.txt'
spark_read_option = spark.read.option("header", "true").option("delimiter", "ขา")

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

# write to cleaned parquet
DF_US_BIBLIO.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_BIBLIO.parquet")
DF_US_IPC.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_IPC.parquet")
DF_US_REL_PSN.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_REL_PSN.parquet")