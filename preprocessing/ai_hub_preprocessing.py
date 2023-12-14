import json
from mrjob.job import MRJob
from mrjob.step import MRStep

class AiHubPreProcess(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_preprocess,
                   reducer=self.reducer_preprocess)
        ]

    def mapper_preprocess(self, _, line):
        data = json.loads(line)

        for aspect in data.get("Aspects", []):
            sentiment_text = aspect.get("SentimentText", "").strip()
            sentiment_polarity = str(aspect.get("SentimentPolarity", "")).strip()

            if sentiment_polarity and sentiment_polarity != "0":
                if sentiment_polarity == "-1":
                    sentiment_polarity = "0"
                yield (sentiment_text, sentiment_polarity)

    def reducer_preprocess(self, key, values):
        for value in values:
            yield (key, value)

if __name__ == '__main__':
    AiHubPreProcess.run()