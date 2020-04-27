import csv
import tqdm

path = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/'
mapping_file = path+'wiki_name_map.txt'
wikidata_file = path+'wikidata_id_name.txt'
wikipedia_file = path+'wikipages202002_new.txt'
wikidata_mapping_file = path+'wikidata_nameid_map.txt'

def load_ID_mapping(mapping_path):
    with open(mapping_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        mapping = {rows[1]:rows[0] for rows in reader}
    row_len = len(mapping)
    print("load {} wiki mapping IDs".format(row_len))
    return mapping



def load_wikidata_mapping(mapping_path):
	par = tqdm.tqdm()
	with open(mapping_path, 'r') as tsvfile:
		id_des_mapping = {}
		id_name_mapping = {}
		for line in tsvfile:
			par.update(1)
			tokens = line.split('\t')
			v = ''
			if len(tokens)>=2:
				ID = tokens[0]
				name = tokens[1]
				id_name_mapping[ID] = name
				if len(tokens)>=3:
					des = tokens[2]
					v += str(des)
					if len(tokens)==4:
						alsoknow=tokens[3]
						v += str(alsoknow)
				id_des_mapping[ID] = v
	row_len = len(id_name_mapping)
	print("load {} wikidata mapping IDs".format(row_len))
	return id_name_mapping, id_des_mapping


def gen_line(id, name, des):
	lines = []
	#<doc id="Q874634" url="https://de.wikipedia.org/wiki?curid=Q874634" title="Oberpollinger">
	#Oberpollinger
	#<a href="Warenhaus">Warenhaus</a> 

	line1 = '<doc id="{}" url="https://de.wikipedia.org/wiki?curid={}" title="{}">\n'.format(str(id), str(id), name)
	line2 = name + '\n'
	line3 = '<a href="{}">{}</a>'.format(name, name) + des+'\n'
	lines.append(line1)
	lines.append(line2)
	lines.append(line3)
	return lines


def integrate():
	wikipedia_name_id_mapping = load_ID_mapping(mapping_file)
	wikidata_id_name_mapping, wikidata_id_des_mapping = load_wikidata_mapping(wikidata_file)
	with open(wikipedia_file, 'a') as wikipedia:
		par = tqdm.tqdm()
		for ID in wikidata_id_name_mapping:
			par.update(1)
			if ID not in wikipedia_name_id_mapping:
				name = wikidata_id_name_mapping[ID]
				des = wikidata_id_des_mapping[ID]
				lines = gen_line(ID, name, des)
				for line in lines:
					wikipedia.write(line)

def gen_wikidata_ID_Name_Mapping_file():
	wikidata_id_name_mapping, wikidata_id_des_mapping = load_wikidata_mapping(wikidata_file)
	print('len wikidata_id_name_mapping', len(wikidata_id_name_mapping))
	with open(wikidata_mapping_file, 'w') as out:
		par = tqdm.tqdm(total = len(wikidata_id_name_mapping))
		for ID in wikidata_id_name_mapping:
			par.update(1)
			if wikidata_id_name_mapping[ID] is not '' or None:
				name = wikidata_id_name_mapping[ID]
				out.write(ID + '\t' + name + '\n')


gen_wikidata_ID_Name_Mapping_file()
integrate()











