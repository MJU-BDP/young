from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, expr, when
from pyspark.sql.types import StructType, StructField, IntegerType
import csv

spark = SparkSession.builder.appName("AdTopic").getOrCreate()

advertisement = spark.read.csv("hdfs:///user/maria_dev/bdp/oliveyoung_advertisement_preprocessed.csv",header=True, inferSchema=True, encoding='UTF-8')

soothing = set(['진정', '자극', '트러블', '여드름', '민감', '어성초', '티트리', '순하다'])
moisturizing = set(['보습', '흡수', '촉촉', '히알루론산', '건조'])
skin = set(['피부결', '부드럽다', '정돈', '장벽', '탄력'])

topics = ['soothing', 'moisturizing', 'skin']
initial_values = {topic: 0 for topic in topics}

for topic in topics:
    advertisement = advertisement.withColumn(topic, lit(initial_values[topic]))
for topic in topics:
    for keyword in eval(topic):
        for i in range(advertisement.count()):
            flag = True
            context = advertisement.select(col('ad')).collect()[i]['ad']

            if keyword in context and flag:
                advertisement = advertisement.withColumn(topic, when(col('_c0') == i, lit(1)).otherwise(col(topic)))
                flag = False

advertisement.show()