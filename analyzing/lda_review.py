from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, CountVectorizer
from pyspark.ml.clustering import LDA

spark = SparkSession.builder.appName("LDAreview").getOrCreate()

review = spark.read.csv('project/oliveyoung_review_preprocessed.csv', header=True, inferSchema=True)

review = review.na.fill({'content': ''})

tokenizer = Tokenizer(inputCol="content", outputCol="words")
wordsData = tokenizer.transform(review)

cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=500)
cvModel = cv.fit(wordsData)
featurizedData = cvModel.transform(wordsData)

lda = LDA(k=3, maxIter=10, seed=0)
ldaModel = lda.fit(featurizedData)

topics = ldaModel.describeTopics(maxTermsPerTopic=100)
vocab = cvModel.vocabulary
for topic in topics.rdd.collect():
    print("Topic: {}".format(topic[0]))
    print(" ".join([vocab[word_idx] for word_idx in topic[1]]))

spark.stop()
