#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import re
from gensim import corpora, models, similarities
from bs4 import BeautifulSoup


class Relevance():

	def relevance(self, content, query):
		#content = re.sub("[^a-zA-Z]", " ", content)
		soup = BeautifulSoup(content, 'html.parser')
		[s.extract() for s in soup(['script','style'])]

		content = [re.sub("[^a-zA-Z]", " ", text) for text in soup.stripped_strings]
		documents = content

		# remove common words and tokenize
		stoplist = set('for a of the and to in is'.split())

		texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

		dictionary = corpora.Dictionary(texts)
		corpus = [dictionary.doc2bow(text) for text in texts]
		#corpora.MmCorpus.serialize('/tmp/deerwester.mm',corpous)
		lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=1)

		#query = "Human computer interaction"
		vec_bow = dictionary.doc2bow(query.lower().split())
		vec_lsi = lsi[vec_bow] # convert the query to LSI space

		index = similarities.MatrixSimilarity(lsi[corpus])
		sims = index[vec_lsi]

		#sims = index[vec_lsi] # perform a similarity query against the corpus
		rel = 0.0
		count = 0 
		for sim in list(enumerate(sims)):
			#print(sim[1])
			rel += sim[1]
			count+=1
		return rel/count

	

