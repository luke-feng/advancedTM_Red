# -*- coding: utf-8 -*-
import re
from tqdm import tqdm
import codecs
import chardet
path = '../end2end_neural_el/deep-ed/basic_data/'
inputfile = path+'dewiki-20200101-page_props.1'
outputfile = path+'id.txt'
mapping = {}
with codecs.open(inputfile, 'r', encoding='utf-8',
                 errors='strict') as inp, open(outputfile, 'w') as out:
	for line in inp:
		ls = line.split(',')
		if len(ls) >= 4:
			_len = (int)(len(ls)/4)
			with tqdm(total = _len) as bar:
				for i in range(_len):
					bar.update(1)
					wikidata_id = ls[i*4 + 2]
					it = re.search(r"Q\d+",wikidata_id)					
					if it is not None:
						wikidata_id = it.group()
						page_id =  re.search(r"\(\d+",ls[i*4])
						if page_id is not None:
							page_id =  re.search(r"\d+",page_id.group()).group()
							mapping[page_id] = wikidata_id
	for key in mapping.keys():
		value = mapping[key]
		line = key + '\t' + value + '\n'
		out.write(line)
					
