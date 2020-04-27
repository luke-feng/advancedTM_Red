import csv
import tqdm
import re
mapping_path ='/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/mapping.tsv'
old_raw_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikipages202002.txt'
new_raw_path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikipages202002_new.txt'


with open(mapping_path, 'r') as tsvfile:
	reader = csv.reader(tsvfile, delimiter='\t')
	mapping = {rows[0]:rows[1] for rows in reader}
row_len = len(mapping)
print("load {} wiki mapping IDs".format(row_len))

def p2q(match):
	pid = match.group()
	if pid in mapping:
		q_id = mapping[pid]
		return q_id
	return pid

bar = tqdm.tqdm()
with open(old_raw_path, 'r') as fin, open(new_raw_path, 'w') as fout:
	for line in fin:
		bar.update(1)
		if '<doc id=' in line:
			info=re.search(r'\d+',line)
			if info is not None:
				new_line = re.sub(r'\d+', p2q, line, count=0)
				fout.write(new_line)
			else:
				fout.write(line)
		else:
			fout.write(line)