import requests
import re
import json
q_not_file= '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/QID_NotInWiki.txt'
basic_url = 'https://www.wikidata.org/wiki/Special:EntityData/'
wiki_file = '/Users/chaofeng/end2end_neural_el/deep-ed/basic_data/wikidata_id_name.txt'

def no_de_entities(file):
    with open(file,'r')as f:
        entities = []
        for line in f:
            entities.append(line.rstrip())
    return entities

def get_webpage(id):
	url = basic_url + str(id) +'.json'
	print(url)
	content = requests.get(url).content
	return content

def get_name_des(content, id):
	data = json.loads(content)
	entities = data['entities']
	cons = entities[id]
	if 'en' not in cons['labels']:
		labels = cons['labels']['fr']['value']
		if 'fr' not in cons['descriptions']:
			descriptions = ''
		else:
			descriptions = cons['descriptions']['fr']['value']
	else:
		labels = cons['labels']['en']['value']
		if 'en' not in cons['descriptions']:
			descriptions = ''
		else:
			descriptions = cons['descriptions']['en']['value']
	return labels, descriptions

def find_entity_name(line):
	patten = re.compile(r'"en":{"language":"en","value":"(.*?)"}')
	a = patten.search(str(line))
	if a is not None:
		return a.group(1)
	else:
		return None

def find_entity_des(line):
    patten = re.compile(r'<div class="wikibase-entitytermsview-heading-description ">(.*?)</div>')
    a = patten.search(str(line))
    if a is not None:
        return a.group(1)
    else:
        return None

entity = no_de_entities(q_not_file)
with open(wiki_file, 'a') as out:
	for e in entity:
		content = get_webpage(e)
		labels, descriptions = get_name_des(content, e)
		line = e+'\t'+labels+'\t' + descriptions+'\n'
		print(line)
		out.write(line)
