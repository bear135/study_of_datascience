from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

DF_US_IPC_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_IPC_Filtered.parquet")    
DF_US_REL_PSN_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_REL_PSN_Filtered.parquet")    
DF_US_BIBLIO_Filtered_read = spark.read.parquet(r"D:/dev-datas/target/DF_US_BIBLIO_Filtered.parquet")    

df_mart = \
    DF_US_IPC_Filtered_read \  
    .join(DF_US_REL_PSN_Filtered_read, on="¹®Çå¹øÈ£", how="left") \
    .join(DF_US_BIBLIO_Filtered_read, on="¹®Çå¹øÈ£", how="left")

# US_DATAMART filtered and write to parquet
df_mart.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_US_DATAMART.parquet")