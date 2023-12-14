from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, CountVectorizer
from pyspark.ml.clustering import LDA

spark = SparkSession.builder.appName("LDAadvertisement").getOrCreate()

data = spark.read.csv('project/oliveyoung_advertisement_preprocessed.csv', header=True, inferSchema=True)

tokenizer = Tokenizer(inputCol="ad", outputCol="words")
wordsData = tokenizer.transform(data)

cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=100)
cvModel = cv.fit(wordsData)
featurizedData = cvModel.transform(wordsData)

lda = LDA(k=3, maxIter=50, seed=1000)
ldaModel = lda.fit(featurizedData)

topics = ldaModel.describeTopics(maxTermsPerTopic=100)
vocab = cvModel.vocabulary
for topic in topics.rdd.collect():
    print("Topic: {}".format(topic[0]))
    print(" ".join([vocab[word_idx] for word_idx in topic[1]]))

spark.stop()
