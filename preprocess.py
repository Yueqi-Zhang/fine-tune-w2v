from input_data import InputData
from input_data import InputVector
from utils import Topfreq, KNeighbor, Batch_pairs, Get_VSP, dump_to_pkl
import numpy
import sys
import codecs

class Word2Vec:
    def __init__(self,
                 input_file_name,
                 input_wvectors,
                 input_word2id,
                 input_id2word,
                 input_topfrequent,
                 output_file_name,
                 window_size=5,
                 min_count=30):
        #data = InputData(input_file_name, min_count)
        word2id = dict()
        with codecs.open(input_word2id, 'r', encoding='utf-8') as f:
            for lines in f:
                word2id[lines.strip().split()[0]] = int(lines.strip().split()[1])
        id2word = dict()
        with codecs.open(input_id2word, 'r', encoding='utf-8') as f:
            for lines in f:
                id2word[int(lines.strip().split()[0])] = lines.strip().split()[1]
        topfrequent = []
        with codecs.open(input_topfrequent, 'r', encoding='utf-8') as f:
            for lines in f:
                topfrequent.append(int(lines.strip()))

        kneighbor = KNeighbor(input_wvectors, topfrequent, word2id, id2word)
        pro_pairs = self.Get_pairs(input_file_name, word2id, id2word, topfrequent, kneighbor, window_size)
        dump_to_pkl(pro_pairs, output_file_name)

    def Get_pairs(self, input_file_name, word2id, id2word, ids, neighbor, window_size):
        pairs = []
        word_count = len(word2id)
        file_name = input_file_name
        words = [id2word[x] for x in ids]
        with codecs.open(file_name, 'r') as f:
            for lines in f:
                lines = lines.strip().split()
                for word in words:
                    if word in lines:
                        sentence_ids = []
                        for w in lines:
                            try:
                                sentence_ids.append(word2id[w])
                            except:
                                continue
                        i = sentence_ids.index(word2id[word])
                        u = word2id[word]
                        c = []
                        for j, v in enumerate(sentence_ids[max(i - window_size, 0):i + window_size + 1]):
                            assert u < word_count
                            assert v < word_count
                            if i < window_size & j == i:
                                continue
                            elif i >= window_size & j == 5:
                                continue
                            else:
                                c.append(v)
                        for n in neighbor[word2id[word]]:
                            pairs.append((u, n, tuple(c)))  # u:center word, n:neighbor, v:context
        return pairs

if __name__ == '__main__':
    w2v = Word2Vec(input_file_name=sys.argv[1], input_wvectors = sys.argv[2], input_word2id = sys.argv[3], input_id2word = sys.argv[4], input_topfrequent = sys.argv[5], output_file_name=sys.argv[6])


