import tqdm
file1 = 'wikidata_nameid_map.txt'
file2 = 'wiki_name_map1.txt'
par = tqdm.tqdm()
with open(file1,'r') as input, open(file2, 'w') as output:
	for line in input:
		par.update(1)
		tokens = line.rstrip().split('\t')
		if len(tokens) == 2:
			ID = tokens[0]
			name = tokens[1]
			new_line = name + '\t' + ID + '\n'
			output.write(new_line)