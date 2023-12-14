import re
from konlpy.tag import Okt
from mrjob.job import MRJob
from mrjob.step import MRStep

class ReviewPreprocessing(MRJob):
    def __init__(self, *args, **kwargs):
        super(ReviewPreprocessing, self).__init__(*args, **kwargs)
        self.okt = Okt()

    def steps(self):
        return [
            MRStep(mapper=self.mapper_review_preprocess,
                   reducer=self.reducer_review_preprocess)
        ]

    def mapper_review_preprocess(self, _, line):
        id, name, date, content = line.split(',')

        content = content.strip()
        content = re.compile('[가-힣]+').findall(content)
        if content:
            content = ' '.join(content)
            content = ' '.join([word for word, tag in self.okt.pos(content)])
            yield id, (name, date, content)

    def reducer_review_preprocess(self, key, values):
        for name, date, content in values:
            yield key, f"{name},{date},{content}"

if __name__ == '__main__':
    ReviewPreprocessing.run()
