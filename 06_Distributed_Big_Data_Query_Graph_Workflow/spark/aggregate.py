from pyspark.sql import SparkSession
s=SparkSession.builder.appName("orders").getOrCreate()
d=s.read.option("header",True).option("inferSchema",True).csv("data/orders.csv")
d.createOrReplaceTempView("orders")
s.sql("SELECT region,SUM(quantity) units,ROUND(SUM(quantity*unit_price),2) revenue FROM orders GROUP BY region ORDER BY revenue DESC").show()
s.stop()
