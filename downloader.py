import logging
import os, sys
from time import localtime, strftime
import urllib
import urllib.parse
import urllib.request
from urllib.error import URLError
from urllib.parse import urlparse, quote_plus
from loggingconfig import LOGGING


class Downloader(object):

	def __init__(self):
		self.logger=logging.getLogger(__name__)
		self.total_requests = 0
		self.total_404errors = 0
		self.total_failed = 0

	def download(self,url):
		
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
		req = urllib.request.Request(url)
		req.add_header('User-Agent', user_agent)
		self.total_requests += 1
		log_header = url + " Response Code: "

		try:

			response = urllib.request.urlopen(req, timeout = 5)
			log_header += str(response.getcode())
			if response.getcode() == 200:
				content_type = response.info().get("content-type")
				content_length = response.info().get("content-length")
				if content_type.startswith("text/html"):
					if content_length:
						file_size = int( content_length or 0)/1000.0
					else:
						file_size = "Unknown"
					
					log_header += " Size: " + str(file_size) + " KB "
					text = response.read()
					self.logger.debug(log_header)
					try:
						self.writer(url, text)
						self.logger.debug(log_header + " has been written to disks!")
						self.crawled_log(strftime("%Y-%m-%d %H:%M:%S", localtime()) +' '+ log_header)
					except :
						self.logger.error(log_header + " CANNOT be written to disks!")
				else:
					log_header += " Unwanted file type, URL discarded "
					return None
				return text
		except URLError as e:
			self.total_failed += 1
			if hasattr(e, 'reason'):
				if hasattr(e, 'code'):
					log_header += str(e.code) + " " + str(e.reason)
					if e.code == 404:
						self.total_404errors += 1
				else:
					log_header += str(e.reason)
				self.logger.error(log_header)
				
		except:
			print(urllib.request.urlopen(req).info())
			self.total_failed += 1
			self.logger.error(url + " Unexpected error happened! ")


	def writer(self, url, text):
		
		url_components = urlparse(url)
		dir = './data/' +url_components.netloc + '/' 
		if not os.path.isdir(dir):
			os.makedirs(dir)
		f = open(dir + quote_plus(url_components.path) +'.txt', 'w')
		f.write(str(text))
		f.close()

	def crawled_log(self, log):
		file = open('focused_crawler_EP500_20.log', 'a')
		file.write(log)
		file.close()

def main():
	downloader = Downloader()
	

if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	main()