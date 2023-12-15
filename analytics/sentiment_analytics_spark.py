
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, regexp_replace
from pyspark.ml.evaluation import BinaryClassificationEvaluator

class SentimentAnalyzer:
    def __init__(self):
        self.spark = SparkSession.builder.appName("SentimentAnalyzer").getOrCreate()
        self.pipeline = None
        self.model = None

    def train_model(self):
        df = self.spark.read.csv('project/ai_hub2.csv', header=True, inferSchema=True, encoding='UTF-8')

        df = df.withColumn('SentimentText', regexp_replace(col('SentimentText'), '[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', ''))
        df = df.withColumn('SentimentText', regexp_replace(col('SentimentText'), '^ +', ''))
        df = df.na.drop(subset=["SentimentText"])

        train, test = df.randomSplit([0.8, 0.2], seed=42)

        tokenizer = Tokenizer(inputCol="SentimentText", outputCol="words")
        hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures")
        idf = IDF(inputCol=hashingTF.getOutputCol(), outputCol="features")
        lr = LogisticRegression(featuresCol='features', labelCol='SentimentPolarity')

        self.pipeline = Pipeline(stages=[tokenizer, hashingTF, idf, lr])

        self.model = self.pipeline.fit(train)
        predictions = self.model.transform(test)

        evaluator = BinaryClassificationEvaluator(labelCol='SentimentPolarity')
        auc = evaluator.evaluate(predictions, {evaluator.metricName: "areaUnderROC"})
        print(f"Test accuracy: {auc}")

    def predict_sentiment(self, sentence):
        if self.model is None:
            raise Exception("train_model()을 통해 모델 학습을 먼저 해야 함.")

        df = self.spark.createDataFrame([(sentence,)], ["SentimentText"])
        result = self.model.transform(df)
        prediction = result.select('prediction').collect()[0][0]
        return 1 if prediction == 1 else 0

analyzer = SentimentAnalyzer()
analyzer.train_model()
print(analyzer.predict_sentiment("보습이 효과가 너무 좋아요"))