import gensim
from gensim.models import Word2Vec
import numpy as np

_len = 300

def load_wordvector(wordvector_path):
	model = Word2Vec.load_facebook_vectors(wordvector_path, binary=True, norm_only=True)

	return model

def get_vector(word, model):
	if word in model:
		return model[word]
	else:
		return np.zeros(_len)





