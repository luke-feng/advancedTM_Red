import logging
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

path = '/Users/chaofeng/Documents/GitHub/advancedTM_Red/data/'
trigram_filename = path + 'wikidata-20200213-truthy-BETA.trigrams.bz2'
#trigram_filename = 'wikidata-20200213-truthy-BETA.trigrams.bz2'
logging.basicConfig(
      format='%(asctime)s : %(levelname)s : %(message)s',
      level=logging.INFO)

sentences = LineSentence(trigram_filename)

filename = path + 'wikidata_cbow300_iter15'
w2v = Word2Vec(sentences, size=300, window=1, min_count=20, workers=20, iter=1)
w2v.save(filename)