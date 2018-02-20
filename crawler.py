import pprint
import logging
import urltools
import urllib
import queue
from urllib import robotparser
from urllib.parse import urlparse
from loggingconfig import LOGGING
from googleapiclient.discovery import build
import pqdict 
from pqdict import maxpq 
from downloader import Downloader
from calculator import Calculator
from Parser import Parser
from w2v import Relevance



#parameters for google search API:
API_KEY="AIzaSyBsx7wuJfoHIA9VsWayDFZW-w7APu-4gps"
SEARCH_ENGINE_ID = '012502276015408778302:aanpptkeffi'


class Crawler():

	def __init__(self):

		self.query = input("Enter search query: ")
		self.webpages_limit = input("Set total number of webpages to be crawled: ")
		self.limit = input("Set limits on how many webpages be crawled from single site: ")
		self.priority_queue = maxpq()
		self.queue = queue.Queue()
		self.downloader = Downloader()
		self.parser = Parser(self.query)
		self.calculator = Calculator(self.query)
		self.relevance = Relevance()
		self.webpages_crawled = 0
		self.logger = logging.getLogger(__name__)
		self.visited_urls = set()
		self.sites_times = {}
	#fetch top 10 results from google search:
	def __fetch_google_results(self):
		service = build("customsearch","v1",developerKey=API_KEY)
		res =service.cse().list(
			q= self.query,
			cx= SEARCH_ENGINE_ID).execute()
		return res
	#enqueue the 10 google search results 
	def enqueue_seeds(self):
		res=self.__fetch_google_results()
		for item in res['items']:
			self.priority_queue.additem(item['link'],10)
			self.queue.put(item['link'])
			self.logger.debug("Enqueued: "+ item['link'])
			
	#check has this url been visited before
	#and has it reach the limit of each site
	#and Robot Exclusion Protocols
	def urlchecker (self, url):
		if url is None:
			return False
		normalized_url = urltools.normalize(url)
		robotparser = urllib.robotparser.RobotFileParser()

		try:
			url_comp = urlparse(normalized_url)
			base_url = url_comp.scheme + "://" + url_comp.netloc + "/"
		except:
			self.logger.error("Cannot parse: " + url)
		try:
			robotparser.set_url(base_url + "robots.txt")
			robotparser.read()
			if not robotparser.can_fetch("*", normalized_url):
				self.logger.error(url + " is excluded due to protocol")
				return False
		except:
			self.logger.error("Cannot determine robots exclusion protocol: " + url)

		if normalized_url in self.visited_urls:
			self.logger.debug(url + " Has been visited before! ")
			return False
		elif base_url in self.sites_times and self.sites_times[base_url] > int(self.limit) :
			#
			self.logger.debug(url + " Times visiting this site have reach the limit ")
			return False
		elif 'cgi' in normalized_url:
			return False
		else:
			return True
	#the crawling process
	def crawl(self):
		try:
			harvest_rate_accum = 0
			while self.webpages_crawled < int(self.webpages_limit):
				print(self.webpages_crawled)
				try:
					url = self.priority_queue.pop()	
				except e:
					print("cannot pop")
				print(url)
				if self.urlchecker(url):
					try:
						content = self.downloader.download(url).decode('utf-8')
						if content is not None:
							self.webpages_crawled += 1
							rel = self.relevance.relevance(content, self.query)
							harvest_rate_accum += rel
							self.crawled_log(" Harvest rate: " + str(harvest_rate_accum / self.webpages_crawled))
					except:
						print( "Failed in downloading")
					normalized_url = urltools.normalize(url)
					try:
						url_comp = urlparse(normalized_url)
						base_url = url_comp.scheme + "://" + url_comp.netloc + "/"
					except:
						self.logger.error("Cannot parse: " + url)
						
					if base_url in self.sites_times:
						self.sites_times[base_url] += 1
					else:
						self.sites_times[base_url] = 1
					self.visited_urls.add(normalized_url)
					
					if rel < 0.2:
						continue
					for link in self.parser.extract_all_links(content):
						full_link = self.parser.parse_links(url, link)
						if full_link is not None:
							link_promise = self.calculator.link_promise(full_link) + rel
							
						try:
							self.priority_queue.additem(full_link, link_promise)
						except:
							pass
		except KeyError :
			print ("Queue is empty now")
			


	def bfs_crawl(self):
		try:
			harvest_rate_accum = 0
			while self.webpages_crawled < int(self.webpages_limit):
				print(self.webpages_crawled)
				try:
					url = self.queue.get()	
				except e:
					print("cannot pop")
				print(url)
				if self.urlchecker(url):
					try:
						content = self.downloader.download(url).decode('utf-8')
						if content is not None:
							self.webpages_crawled += 1
							rel = self.relevance.relevance(content, self.query)
							harvest_rate_accum += rel
							self.crawled_log(" Harvest rate: " + str(harvest_rate_accum / self.webpages_crawled))
					except:
						print( "Failed in downloading")
					normalized_url = urltools.normalize(url)
					try:
						url_comp = urlparse(normalized_url)
						base_url = url_comp.scheme + "://" + url_comp.netloc + "/"
					except:
						self.logger.error("Cannot parse: " + url)
					self.visited_urls.add(normalized_url)
					
					for link in self.parser.extract_all_links(content):
						full_link = self.parser.parse_links(url, link)
						if full_link is not None :
							try:
								if base_url  not in self.sites_times:
									self.sites_times[base_url] = 1
								elif self.sites_times[base_url] < int(self.limit):
									self.sites_times[base_url] += 1
								else:
									continue
								self.queue.put(full_link)
							except:
								pass
		except KeyError :
			print ("Queue is empty now")

	def crawled_log(self, log):
		file = open('demo.log', 'a')
		file.write(log+'\n\n')
		file.close()

def main():
	crawler = Crawler()
	crawler.enqueue_seeds()
	bfs = input(" BFS or not?(y/n): ")
	if bfs:
		crawler.bfs_crawl()
	else:
		crawler.crawl()
	statistics = "Total request: " + str(crawler.downloader.total_requests) + " Total 404 encountered: " + str(crawler.downloader.total_failed)
	crawler.crawled_log(statistics)
	

if __name__ == '__main__':
	import logging.config
	logging.config.dictConfig(LOGGING)
	#logging.config.fileConfig('logging1.config',disable_existing_loggers=False)
	main()
