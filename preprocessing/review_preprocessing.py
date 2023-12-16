import re
import subprocess
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
        proc = subprocess.Popen(['hadoop', 'fs', '-cat', 'project/stop_words.txt'], stdout=subprocess.PIPE)
        stopwords = proc.stdout.read().decode('utf-8').split()

        if content:
            content = ' '.join(content)
            content = ' '.join([word for word, tag in self.okt.pos(content)])
            token = [t for (t, pos) in self.okt.pos(content, stem=True) if
                     pos in ['Noun', 'Verb', 'Adjective'] and t not in stopwords and len(t) > 1]

            preprocessed_content = ' '.join(token)
            yield id, (name, date, preprocessed_content)

    def reducer_review_preprocess(self, key, values):
        for name, date, content in values:
            yield key, f"{name},{date},{content}"

if __name__ == '__main__':
    ReviewPreprocessing.run()
