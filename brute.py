import math
import pdb

NEWS_FILE = './news.txt'
IDF_FILE = './news.idf.txt'
BRUTE_FILE = './brute.top'
DEFAULT_IDF = 13.6332

class Brute():
    def __init__(self, N):
        self.N = N

        self._id = 0
        self.current_news = ""
        self.news = {}
        self.vocabulary = []
        self.position_map = {}
        self.unit_length = {}
        self.read_idf()

        self.dw = dict()

        self.brute()

    def brute(self):
        # initialization
        # self.read_news_into_buffer()
        # self.read_news_imp(0)
        self.read_news(0)
        self.update_vocabulary()
        self.compute_qw()
        self.update_unit_length()

        self.df = dict()

        for i in range(1, self.N):
            # expand the collection of past news
            self.expand_news()
            self.update_dw()

            # read more news
            self.read_news(i)
            # self.read_news_imp(i)
            self.update_vocabulary()
            self.compute_qw()
            self.update_unit_length()
            # self.compute_dw()
            # self.cosine_similarity()
            # self.cosine_similarity_imp()
            self.cosine_similarity_imp_2()

            # write result
            self.write_result()

            # reset
            self.df = dict()

    def read_idf(self):
        self._idf = dict()
        with open(IDF_FILE) as f:
            for line in f:
                temp = line.strip().split()
                idf = float(temp[0])
                token = temp[1]

                self._idf[token] = idf

    def get_idf(self, token):
        if token in self._idf:
            return self._idf[token]
        else:
            return DEFAULT_IDF

    def get_pos(self, token):
        try:
            return self.position_map[token]
        except KeyError:
            return -1

    def read_news(self, i):
        count = 0

        with open(NEWS_FILE) as f:
            for line in f:
                if count == i:
                    temp = line.lower().split()
                    self._id = temp[0]
                    self.current_news = temp[1:]

                count += 1

    def read_news_imp(self, i):
        line = self.buffer[i]
        temp = line.lower().split()
        self._id = temp[0]
        self.current_news = temp[1:]

    def read_news_into_buffer(self):
        self.buffer = []

        with open(NEWS_FILE) as f:
            for line in f:
                self.buffer.append(line.strip())

    def update_vocabulary(self):
        for token in self.current_news:
            l = len(self.vocabulary)

            if token not in self.vocabulary:
                self.vocabulary.append(token)
                self.position_map[token] = l

    def expand_news(self):
        self.news[self._id] = self.current_news

    def compute_qw(self):
        self.qw = [0 for i in range(len(self.vocabulary))]

        for token in set(self.current_news):
            count = self.current_news.count(token)
            try:
                self.qw[self.position_map[token]] = count
                self.qw[self.position_map[token]] *= self.get_idf(token)
            except KeyError:
                pass

    def update_dw(self):
        self.dw[self._id] = self.qw

    def compute_dw(self):
        self.dw = dict()

        for (_id, news) in self.news.iteritems():
            self.dw[_id] = [0 for i in range(len(self.vocabulary))]
            C = len(self.news)

            for token in set(news):
                pos = self.position_map[token]

                # compute term frequency
                count = news.count(token)
                try:
                    self.dw[_id][pos] = count
                    self.dw[_id][pos] *= self.get_idf(token)
                except KeyError:
                    pass

    def dot_product(self, vector_1, vector_2):
        l = len(vector_1)
        
        if len(vector_1) != len(vector_2):
            print "Error in dot product calculation"

        summation = 0
        for i in range(l):
            summation += vector_1[i] * vector_2[i]
        
        unit_length_1 = self.unit_length(vector_1)
        unit_length_2 = self.unit_length(vector_2)

        value = 0 
        try:
            value = (summation * 1.0) / (unit_length_1 * unit_length_2)
        except ZeroDivisionError:
            print "zero division error in dot product"

        return value

    def unit_length_imp(self, vector, pos):
        sum_square = 0

        for i in pos:
            sum_square += pow(vector[i], 2)

        return pow(sum_square, 0.5)

    def dot_product_imp(self, vector_1, vector_2, pos_1, pos_2):        
        if len(vector_1) != len(vector_2):
            print "Error in dot product calculation"

        summation = 0
        for i in pos_1:
            summation += vector_1[i] * vector_2[i]
        
        unit_length_1 = self.unit_length_imp(vector_1, pos_1)
        unit_length_2 = self.unit_length_imp(vector_2, pos_2)

        value = 0 
        try:
            value = (summation * 1.0) / (unit_length_1 * unit_length_2)
        except ZeroDivisionError:
            print "zero division error in dot product"

        return value

    def cosine_similarity(self):
        self.score = []

        for (_id, vector) in self.dw.iteritems():
            _score = self.dot_product(self.qw, vector)

            self.score.append((_id, _score))

    def cosine_similarity_imp(self):
        self.score = []

        for (_id, vector) in self.dw.iteritems():
            s1 = set(self.current_news)
            s2 = set(self.news[_id])
            pos_1 = [self.get_pos(token) for token in s1]
            pos_2 = [self.get_pos(token) for token in s2]

            _score = self.dot_product_imp(self.qw, vector, pos_1, pos_2)

            self.score.append((_id, _score))

    def update_unit_length(self):
        s1 = set(self.current_news)
        pos = [self.get_pos(token) for token in s1]
        ul = self.unit_length_imp(self.qw, pos)

        self.unit_length[self._id] = ul

    def cosine_similarity_imp_2(self):
        self.score = []

        for (_id, vector) in self.dw.iteritems():                
            vector_1 = self.qw
            vector_2 = vector

            s1 = set(self.current_news)
            pos_1 = [self.get_pos(token) for token in s1]

            summation = 0
            for i in pos_1:
                try:
                    summation += vector_1[i] * vector_2[i]
                except IndexError:  
                    summation = summation

                unit_length_1 = self.unit_length[self._id]
                unit_length_2 = self.unit_length[_id]

            _score = 0 
            try:
                _score = (summation * 1.0) / (unit_length_1 * unit_length_2)

                if self._id == '8' and _id == '2':
                    print summation
                    print unit_length_1 * unit_length_2
                    print _score
            except ZeroDivisionError:
                print "zero division error in dot product"

            self.score.append((_id, _score))

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

    def write_result(self):
        id_and_score = self.get_most_similar_news()

        if id_and_score[1] >= 0.2:
            with open(BRUTE_FILE, 'a') as output:
                output.write('%s %s\n' % (self._id, id_and_score))
                # output.write('%s %s\n' % (self._id, id_and_score[0]))