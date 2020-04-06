# -*- coding: utf-8 -*-
import os
import tqdm.tqdm
root = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/textWithAnchorsFromAllDeWikipedia202002'
output_file = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/data/textWithAnchorsFromAllDeWikipedia202002.txt'
with open(output_file, 'w') as o:
	for dirName, subdirList, fileList in os.walk(root):
	    print('Found directory: %s' % dirName)
	    for fname in fileList:
	    	print(fname)
	    	if fname == '.DS_Store':
	    		continue
	    	else:
	    		with open(dirName + '/'+fname) as f:
	    			for line in f:
	    				o.write(line)

