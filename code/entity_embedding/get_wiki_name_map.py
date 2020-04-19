import json
import warnings
import tqdm
import re
import sys
import csv
import os
from nltk.tokenize import word_tokenize
from bz2 import BZ2File
from multiprocessing import Pool
warnings.filterwarnings('ignore')
wikidata_path = '../end2end_neural_el/deep-ed/basic_data/wikidata/'
wiki_name_map = '../end2end_neural_el/deep-ed/basic_data/wiki_name_map.txt'
mapping_path ='../end2end_neural_el/deep-ed/basic_data/mapping.tsv'

def filter_tokens(tokens):
	for t in tokens:
		if not DROP_TOKEN_RE.match(t):
			yield t.lower()

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
    _title = article_json["title"]
    return _id, _title

def load_ID_mapping(mapping_path):
    with open(mapping_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        mapping = {rows[0]:rows[1] for rows in reader}
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping

def main():
    pool = Pool(8)
    art = 0
    mapping = load_ID_mapping(mapping_path)
    with open(wiki_name_map, 'w') as fout:
        tbar = tqdm.tqdm()
        for _id, _title in pool.imap_unordered(process_line, get_lines(wikidata_path)):
            if _id in mapping:
                _id = mapping[_id]
                fout.write(_title + "\t" + _id +"\n")
                art += 1
            tbar.update(1)

                
            
    pool.terminate()
    print("Finished %d.", art)

if __name__ == "__main__":
    sys.exit(main())