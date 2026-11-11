from pyspark.sql import SparkSession
from pyspark.sql.types import *
s=SparkSession.builder.appName("stream").getOrCreate()
schema=StructType([StructField("event_id",LongType()),StructField("device",StringType()),StructField("kind",StringType()),StructField("value",DoubleType())])
s.readStream.schema(schema).json("stream/in").groupBy("kind").count().writeStream.outputMode("complete").format("console").option("checkpointLocation","stream/checkpoint").start().awaitTermination()
