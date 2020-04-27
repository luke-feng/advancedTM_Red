from bz2 import BZ2File
import bz2
import re
import tqdm
import json

file1 = 'wikidata-2019-11-13.nt.bz2'
file2 = 'latest-all.json.bz2'
filepath = '/Users/chaofeng/end2end_neural_el/new_data/' + file2
temp_file  = '/Users/chaofeng/end2end_neural_el/new_data/' + 'temp1.txt'
q_not_file= '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/QID_NotInWiki.txt'

def find_Qid(line):
    patten = re.compile(r'{"type":"item","id":"(.*?)"')
    a = patten.search(line)
    if a is not None:
        return a.group(1)
    else:
        return None

def no_de_entities(file):
    with open(file,'r')as f:
        entities = []
        for line in f:
            entities.append(line.rstrip())
    return entities

def open_bz_file(filepath):
    if filepath.endswith(".bz2"):
        return bz2.open(filepath, mode='rt')
    else:
        return open(filepath)

def process(file):
    count = 0
    bar = tqdm.tqdm()
    no_de_entity = no_de_entities(q_not_file)
    co = 0
    with open(temp_file, 'w') as temp:
        for line in file:
            count += 1
            qid = find_Qid(line)
            bar.update(1)
            if qid not in no_de_entity and qid is not None:
                new_line = ''
                try:
                    data = json.loads(line.rstrip(',\n'))
                    id = data['id']
                    if id in no_de_entity:
                        new_line += id  
                        if 'Q' in id and 'labels' in data:
                            labels = data['labels']
                            if 'en' in labels:
                                de = labels['en']
                                value_labels = de['value']
                                new_line += '\t' + value_labels
                            elif 'fr' in labels:
                                de = labels['fr']
                                value_labels = de['value']
                                new_line += '\t' + value_labels  
                        if 'descriptions' in data:
                            descriptions = data['descriptions']
                            if 'de' in descriptions:
                                de_d = descriptions['de']
                                value_descriptions = de_d['value']
                                new_line += '\t' + value_descriptions
                        if 'aliases' in data:
                            aliases = data['aliases']
                            if 'de' in aliases:
                                de_a= aliases['de'][0]
                                value_aliases = de_a['value']
                                new_line += '\t' + value_aliases
                            temp.write(new_line + '\n')    
                except json.decoder.JSONDecodeError:
                    continue

            #temp.write(str(data) + '\n')


file = open_bz_file(filepath)
process(file)
