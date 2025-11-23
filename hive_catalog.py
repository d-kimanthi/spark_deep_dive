from pyspark.sql import SparkSession

spark_session_hive = (
    SparkSession.builder.master(spark.conf.get("spark.master"))
    .config(conf=spark.sparkContext.getConf())
    .appName("hive-support")
    .enableHiveSupport()
    .getOrCreate()
)

spark_session_hive.sql("show databases;").show()

db_name = "coffee_co_common"
db_description = (
    "This database stores common information regarding inventory, stores, and customers"
)

default_warehouse = spark.catalog.getDatabase("default").locationUri
warehouse_prefix = f"{default_warehouse}/common"

spark.sql(
    f"""
CREATE DATABASE IF NOT EXISTS {db_name}
COMMENT '{db_description}'
LOCATION '{warehouse_prefix}'
WITH DBPROPERTIES(TEAM='core',LEAD='scott',TEAM_SLACK='#help_coffee_common');
"""
)


jdbc_driver = "com.mysql.cj.jdbc.Driver"
db_host = "mysql"
db_port = "3306"
default_db = "default"
db_table = "bettercustomers"
db_user = "dataeng"
db_pass = "dataengineering_user"

connection_url = f"jdbc:mysql://{db_host}:{db_port}/{default_db}"

better_customers = (
    spark_session_hive.read.format("jdbc")
    .option("url", connection_url)
    .option("driver", jdbc_driver)
    .option("dbtable", "bettercustomers")
    .option("user", db_user)
    .option("password", db_pass)
    .load()
)

better_customers.createOrReplaceTempView("customers")
better_customers.show()


coffee_co_database_name = "coffee_co_common"

spark_session_hive.catalog.setCurrentDatabase(coffee_co_database_name)

better_customers.write.mode("overwrite").saveAsTable("customers")
