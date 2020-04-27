# -*- coding: utf-8 -*-
import gensim
import csv
from gensim.models.fasttext import FastText
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim import utils
import numpy as np
from collections import Counter
import logging
import json
import re
import sys
import os
from nltk.tokenize import word_tokenize
from bz2 import BZ2File
from multiprocessing import Pool
from numpy import zeros, dtype, float32 as REAL, ascontiguousarray, fromstring
import warnings
import tqdm

warnings.filterwarnings('ignore')

_len = 300
DROP_TOKEN_RE = re.compile("^\W*$")
wordvector_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/cc.de.300.bin'
idf_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikidata_tfidf_terms.csv'
wikidata_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikidata/'
cpus = 6
p2v_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wiki_p2v.bin'
mapping_path ='/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/mapping.tsv'
temp_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/temp.txt'

def filter_tokens(tokens):
	for t in tokens:
		if not DROP_TOKEN_RE.match(t):
			yield t.lower()


def load_model(wordvector_path):
    model = gensim.models.fasttext.load_facebook_vectors(wordvector_path, encoding='utf-8')
    word_num = len(model.vocab)
    print('loaded {} words to model'.format(word_num))
    return model

def get_vector(word, model):
    if word in model:
        return model[word]
    else:
        return np.zeros(_len)

def get_embedded_entities(temp_path):
    entites = {}
    with open(temp_path, 'r') as temp:
        for line in temp:
            tokens = line.split(" ")
            entites.add(tokens[0])
    print("{} entities have been processed".format(len(entites)))
    return entites


def load_idf(idf_path):
    with open(idf_path, 'r') as infile:
        reader = csv.reader(infile)
        idfdict = {rows[0]:rows[3] for rows in reader}
    row_len = len(idfdict)
    print('loaded {} words to idf_dict'.format(row_len))
    return idfdict

def get_idf(word, idfdict):
    if word in idfdict:
        return idfdict[word]
    else:
        return 0.0000001


def get_file_reader(filename):
    if filename.endswith(".bz2"):
        return BZ2File(filename)
    else:
        return open(filename)


def get_lines(input_files):
    n = 1
    for dirName, subdirList, fileList in os.walk(input_files):
        n += 1
        for fname in fileList:
            if fname == '.DS_Store':
                continue
            else:
                with get_file_reader(dirName + '/'+fname) as f:
                    for line in f:
                        yield line

def process_line(line):
    article_json = json.loads(line)
    _id = article_json["id"]
    tokens = set(filter_tokens(word_tokenize(article_json["text"])))
    return _id, tokens


def save_word2vec_format(page_vec, p2v_path=p2v_path, binary=True):
    total_vec = len(page_vec)
    voctor_size = _len
    with utils.open(p2v_path, 'wb') as fout:
        fout.write(utils.to_utf8("%s %s\n" % (total_vec, voctor_size)))
        for word, row in page_vec.items():
            if binary:
                row = row.astype(REAL)
                fout.write(utils.to_utf8(word) + b" " + row.tostring())
            else:
                fout.write(utils.to_utf8("%s %s\n" % (word, ' '.join(repr(val) for val in row))))

def load_ID_mapping(mapping_path):
    with open(mapping_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        mapping = {rows[0]:rows[1] for rows in reader}
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping

def get_wikidataID(id, mapping):
    id = str(id)
    if id in mapping:
        return mapping[id]
    else:
        return 'OutOfList'

def get_p2v(tokens, model, idfdict):
    # e_p = sum(e_w * idf_w) / sum(idf_w)
    text_len = len(tokens)
    sum_ew = np.zeros(_len)
    sum_idf = 0.0
    for token in tokens:
        t_v = get_vector(token, model)
        idf = float(get_idf(token, idfdict))
        sum_ew += t_v * idf
        sum_idf += idf
    p2v = sum_ew / sum_idf
    return p2v


def main():
    tokens_c = Counter()
    articles = 0
    pool = Pool(cpus)
    entites = get_embedded_entities(temp_path)
    model = load_model(wordvector_path)
    idfdict = load_idf(idf_path)
    mapping = load_ID_mapping(mapping_path)

    with utils.open(temp_path, 'ab') as fout:
        tbar = tqdm.tqdm(total = len(mapping_path))
        for _id, tokens in pool.imap_unordered(process_line, get_lines(wikidata_path)):
            articles +=1
            tbar.update(1)
            tokens_c.update(tokens)
            wikeID = get_wikidataID(_id, mapping)
            if wikeID in entites:
                continue
            else:
                vec = get_p2v(tokens, model, idfdict)
                fout.write(utils.to_utf8("%s %s\n" % (wikeID, ' '.join(repr(val) for val in vec))))
            

    pool.terminate()
    print("Finished, Done %d articles.", articles)

if __name__ == "__main__":
    sys.exit(main())