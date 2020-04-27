from bz2 import BZ2File
import re

path = '/Users/chaofeng/Documents/GitHub/advancedTM_Red/data/'
dump_filename = path + 'wikidata-20200213-truthy-BETA.nt.bz2'
trigram_filename = path + 'wikidata-20200213-truthy-BETA.trigrams'

pattern = re.compile(
        (r'^<http://www.wikidata.org/entity/(Q\d+)> '
         r'<http://www.wikidata.org/prop/direct/(P\d+)> '
         r'<http://www.wikidata.org/entity/(Q\d+)>'),
         flags=re.UNICODE)

with open(trigram_filename, 'w') as f:
    for line in BZ2File(dump_filename):
        line = line.decode('utf-8')
        match = pattern.search(line)
        if match:
            f.write(" ".join(match.groups()) + '\n')