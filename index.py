import pdb
import time
import os

NEWS_FILE = './news.txt'
IDF_FILE = './news.idf.txt'
INDEX_FILE = './index.top'
DEFAULT_IDF = 13.6332

class Index():
    def __init__(self, N):
        a = 2
        self.N = N

        self._idf = dict()
        self.id_map = []
        self.all_news = []
        self.vocab = []
        self.position_map = dict()
        self.tf = []
        self.tfidf = []
        self.unit_length = []
        self.ii = dict() # inverted index

        self.saved_score = []

        self.index()

    def print_time(self, msg, t):
        print '%s ====================== %f' % (msg, t)

    def index(self):        
        self.read_N_news()
        
        self.read_idf()

        self.calculate_tfidf()

        self.calculate_unit_length()

        self.inverted_index()

        # query_index instead of id
        for index in range(1, self.N):
            self.linear_merge(index)
            self.analyze_matching_set(index)

        self.write_result(index)

    def read_idf(self):
        self._idf = dict()

        with open(IDF_FILE) as f:
            for line in f:
                temp = line.strip().split()
                idf = float(temp[0])
                token = temp[1]

                self._idf[token] = idf

    def idf(self, token):
        if token in self._idf:
            return self._idf[token]
        else:
            return DEFAULT_IDF

    def read_N_news(self):
        with open(NEWS_FILE) as f:
            # real work starts here
            for i in range(self.N):
                line = f.readline().strip().lower().split()
                self.id_map.append(line[0])
                self.all_news.append(line[1:])
    
    def build_vocabulary(self):
        count = 0
        for news in self.all_news:
            for token in set(news):
                if token not in self.vocab:
                    self.vocab.append(token)
                    self.position_map[token] = count
                    count += 1

    def calculate_tfidf(self):
        for (i, news) in enumerate(self.all_news):
            _tfidf = dict()
            for token in set(news):
                tf = news.count(token)
                _tfidf[token] = tf * self.idf(token)
            self.tfidf.append(_tfidf)

    def calculate_unit_length(self):
        for (index, tfidf) in enumerate(self.tfidf):
            sum_square = 0
            for count_value in tfidf.values():
                sum_square += pow(count_value, 2)

            self.unit_length.append(pow(sum_square, 0.5))

    def inverted_index(self):
        for (index, news) in enumerate(self.all_news):
            tf = self.tfidf[index]
            for (token, count) in tf.iteritems():
                if token not in self.ii:
                    self.ii[token] = []

                self.ii[token].append((index, count))

    def linear_merge(self, query_index):
        query_tfidf = self.tfidf[query_index]

        # question
        max_doc_index = query_index

        self.matching_set = [0 for j in range(max_doc_index)]
        
        for (token, qw) in query_tfidf.iteritems():
            _ii = self.ii[token]
            for (doc_index, count) in _ii:
                if doc_index < max_doc_index:
                    self.matching_set[doc_index] += count * qw
                else:
                    break

    def analyze_matching_set(self, query_index):
        self.score = []
        col = len(self.matching_set)

        query_tfidf_array = self.tfidf[query_index].values()

        for doc_index in range(col):
            summation = self.matching_set[doc_index]
            _score = summation / (self.unit_length[query_index] * self.unit_length[doc_index])
            self.score.append((doc_index, _score))

        self.saved_score.append(self.get_most_similar_news())

    def get_most_similar_news(self):
        sorted_score = sorted(self.score, key=lambda x:x[1], reverse=True)
        
        _id = 0
        top_score = sorted_score[0][1]
        smallest_id = int(sorted_score[0][0])

        for i in range(1, len(sorted_score)):
            if sorted_score[i][1] == top_score:
                if smallest_id > int(sorted_score[i][0]):
                    smallest_id = int(sorted_score[i][0])
                    _id = i
            else:
                break

        return sorted_score[_id]

    def write_result(self, query_index):
        with open(INDEX_FILE, 'a') as output:
            for (query_index, id_and_score) in enumerate(self.saved_score):
                if id_and_score[1] >= 0.2:
                    output.write('%d %d\n' % (query_index + 2, int (id_and_score[0]) + 1))

if __name__ == '__main__':
    if os.path.isfile('./index.top'):
        os.remove('./index.top')

    N = 5000
    index = Index(N)
