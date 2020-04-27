from bz2 import BZ2File
import bz2
import re
import tqdm
import json

file2 = 'latest-all.json.bz2'
filepath = '/Users/chaofeng/end2end_neural_el/new_data/' + file2
temp_file  = '/Users/chaofeng/end2end_neural_el/new_data/' + 'wikidata_id_name.txt'
def open_bz_file(filepath):
    if filepath.endswith(".bz2"):
        return bz2.open(filepath, mode='rt')
    else:
        return open(filepath)

def process(file, maxcount):
    count = 0
    bar = tqdm.tqdm()
    with open(temp_file, 'w') as temp:
        for line in file:
            count += 1
            bar.update(1)
            new_line = ''
            try:
                data = json.loads(line.rstrip(',\n'))
                id = data['id']
                new_line += id  
                if 'Q' in id and 'labels' in data:
                    labels = data['labels']
                    if 'de' in labels:
                        de = labels['de']
                        value_labels = de['value']
                        new_line += '\t' + value_labels
                    elif 'en' in labels:
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
process(file, 300)
