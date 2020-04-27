import numpy as np
from numpy import zeros, dtype, float32 as REAL, ascontiguousarray, fromstring
from gensim import utils
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import tqdm
temp_path = '/Users/chaofeng/Downloads/2014_tudarmstadt_german_5mincount.vocab'
p2v_path = '/Users/chaofeng/Downloads/2014_tudarmstadt_german_5mincount.bin'
def read_temp(temp_path):
    vocab = dict()
    bar = tqdm.tqdm()
    line_num = 0
    with open(temp_path, 'r') as temp:
        for line in temp:
            ls = line.split(" ")
            val = np.asarray(ls[1:], dtype=np.float32)
            vocab[ls[0]] = val
            bar.update(1)
            line_num +=1
    print(vocab["der"])
    bar.close()
    return vocab


def save_word2vec_format(page_vec, p2v_path=p2v_path, binary=True):
    total_vec = len(page_vec)
    voctor_size = len(page_vec["der"])
    print(total_vec, voctor_size)
    bar = tqdm.tqdm()
    with utils.open(p2v_path, 'wb') as fout:
        fout.write(utils.to_utf8("%s %s\n" % (total_vec, voctor_size)))
        for word, row in page_vec.items():
            bar.update(1)
            if binary:
                row = row.astype(REAL)
                fout.write(utils.to_utf8(word) + b" " + row.tostring())
            else:
                fout.write(utils.to_utf8("%s %s\n" % (word, ' '.join(repr(val) for val in row))))
    bar.close()

page_vec = read_temp(temp_path)
save_word2vec_format(page_vec, p2v_path=p2v_path, binary=True)
wv_from_bin = KeyedVectors.load_word2vec_format(datapath(p2v_path), binary=True)
vec = wv_from_bin["der"]
print(vec)