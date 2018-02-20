import re
import collections
import logging
from math import log, sqrt
from porter2stemmer import Porter2Stemmer
from loggingconfig import LOGGING

class Calculator(object):
	def __init__(self, query):
		self.tfidf_query = {}
		self.query_terms = re.findall("\w+", query)
		query_terms_count = collections.Counter(self.query_terms)
		print(query_terms_count)
		for term in self.query_terms:
			if term in query_terms_count:
				self.tfidf_query[term] = 1 + log(query_terms_count[term])
			else:
				self.tfidf_query[term] = 0
		


	def link_promise(self, link):
		promise = 0.0
		stemmer = Porter2Stemmer()
		if link is None:
			return promise
		try:
			#get terms in the link
			link_terms = re.findall("\w+", link.lower())
			link_terms = [stemmer.stem(term) for term in link_terms]

		except:
			print("link error")
			return promise
		#get terms in the query
		link_terms_count = collections.Counter(link_terms)
		self.query_terms = [stemmer.stem(term) for term in self.query_terms]
		#calculate promise
		for term in self.query_terms:
			if term in link_terms_count:
				promise = promise + 0.1 * link_terms_count[term]
		return promise



if __name__ == '__main__':
	main()

