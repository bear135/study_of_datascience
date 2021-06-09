from pyspark.sql.session import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext
conf = (SparkConf().setMaster("local[*]").setAppName("Python").set("spark.executor.memory", "8g").set('spark.driver.memory','4g').set('spark.driver.maxResultsSize','0'))
sc = SparkContext(conf = conf)
spark = SparkSession(sc)

# ipcmaster csv file to parquet
DF_IPCMASTER = spark.read.options(header='true').csv(r"D:/rawdata/IPCMASTER.csv")
DF_IPCMASTER.repartition(1).write.mode("overwrite").parquet(r"D:/dev-datas/target/DF_IPCMASTER.parquet")

