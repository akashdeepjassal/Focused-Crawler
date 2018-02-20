import logging
from loggingconfig import LOGGING
import urltools
import urllib
from urllib.parse import urlparse

visited_urls = {}
sites_times = {}

def urlchecker (url, limit):
	normalized_url = urltools.normalize(url)
	url_comp = urlparse(url)
	if visited_urls.has_key(url):
		return False
	elif times_visiting_site[url_comp.net_loc] > limit :
		visited_urls[url] = True
		return False
	else:
		return True



