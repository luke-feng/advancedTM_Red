# -*- coding: utf-8 -*-
'''import gensim
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim import utils
wordvector_path = '/Users/chaofeng/Downloads/2014_tudarmstadt_german_5mincount.vocab'

with open()


def load_model(wordvector_path):
    model = KeyedVectors.load_word2vec_format(wordvector_path, binary=False)
    word_num = len(model.vocab)
    print('loaded {} words to model'.format(word_num))
    return model

load_model(wordvector_path)'''
in_filepath = '/Users/chaofeng/end2end_neural_el/data/basic_data/test_datasets/HIPE/'
infiles = ['HIPE-data-v1.0-train-de.tsv','HIPE-data-v1.0-dev-de.tsv']
out_filepath = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/QID_HIPE.txt'
mapping_path ='/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikidata_nameid_map.txt'
q_file= '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/QID.txt'
q_not_file= '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/QID_NotInWiki.txt'
def load_ID_mapping(mapping_path):
    mapping = {}
    with open(mapping_path, 'r') as tsvfile:
        for line in tsvfile:
            tokens = line.split('\t')
            if len(tokens) == 2:
                mapping[tokens[0]] = tokens[1]
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping


qid = load_ID_mapping(mapping_path)

print(len(qid))
count_in = 0
count_not_in = 0
hipe_qid = {}

for file in infiles:
    with open(in_filepath+file, 'r') as infs, open(out_filepath, 'w') as outs:
        for line in infs:
            li = line.split('\t')
            if len(li) == 10 and 'Q' in li[7]:
                hipe_qid[li[7]] = ''
with open(q_not_file,'w') as notin:
    for hq in hipe_qid:
        if hq not in qid:
            count_not_in += 1
            notin.write(hq+'\n')

print(count_not_in)
        
