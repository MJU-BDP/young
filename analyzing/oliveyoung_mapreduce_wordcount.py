import sys
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol
import csv
import pandas as pd

class WordCountInThreeListsMRJob(MRJob):

    def configure_args(self):
        super(WordCountInThreeListsMRJob, self).configure_args()
        self.add_file_arg('--wordlist1', help='Path to the first file containing the word list')
        self.add_file_arg('--wordlist2', help='Path to the second file containing the word list')
        self.add_file_arg('--wordlist3', help='Path to the third file containing the word list')

    def mapper_init(self):
        self.wordlists = {}

        for i in range(1, 4):  # Assuming you have 3 word lists
            wordlist_path = getattr(self.options, f'wordlist{i}')
            with open(wordlist_path, 'r', encoding="utf-8") as f:
                wordlist_name = wordlist_path.split('.')[0]

                self.wordlists[wordlist_name] = set(f.read().split())

    def mapper(self, _, line):
        df_row = next(csv.reader([line]))
        document = df_row[4]  # Assuming the document is in the 4th column

        words = document.split()  # You may need to adjust this based on your document format
        
        word_counts = {}
        for wordlist_name, wordlist in self.wordlists.items():
            word_counts[wordlist_name] = 0 #set 0
            for word in words:
                if word in wordlist:
                    word_counts[wordlist_name] += 1

        for wordlist_name, count in word_counts.items():
            yield(wordlist_name, count)


    def combiner(self, wordlist_name, counts):
        yield(wordlist_name, sum(counts))

    def reducer(self, wordlist_name, counts):
        df = pd.dataFrame({wordlist_name: [sum(counts)]})
        csv_out = df.to_csv(index=False)
        yield(None, csv_out)

if __name__ == '__main__':
    WordCountInThreeListsMRJob.run()
