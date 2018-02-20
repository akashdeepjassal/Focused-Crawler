from linksExtractor import MyHTMLParser
import urllib
import os
from urllib.parse import urlparse

class Parser(object):
	

	def __init__(self, query):
		self.query = query
		

	def extract_all_links(self, content):
		my_html_parser = MyHTMLParser()
		my_html_parser.feed(content)

		return my_html_parser.links

	#filter unwanted links and return a full link
	def parse_links(self, url, link):
		IGNORED_EXTENSIONS = [
        # images
        '.mng', '.pct', '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.pst', '.psp', '.tif',
        '.tiff', '.ai', '.drw', '.dxf', '.eps', '.ps', '.svg',

        # audio
        '.mp3', '.wma', '.ogg', '.wav', '.ra', '.aac', '.mid', '.au', '.aiff',

        # video
        '.3gp', '.asf', '.asx', '.avi', '.mov', '.mp4', '.mpg', '.qt', '.rm', '.swf', '.wmv',
        '.m4a',

        # other
        '.css', '.pdf', '.doc', '.exe', '.bin', '.rss', '.zip', '.rar', '.docx', '.xls', '.xlsx',
        '.js', '.ppt', '.pptx',	]

		#WEBSITE_BLACKLIST = [ 'www.amazon.com', 'www.amazon.co.uk', 'amzn.to']

		try:
			url_components = urlparse(link)
			root, ext = os.path.splitext(url_components.path)
		except:
			return
	
		if ext in IGNORED_EXTENSIONS or ext in (item.upper() for item in IGNORED_EXTENSIONS):
			return
		#if url_components.netloc in WEBSITE_BLACKLIST:
			#return 
		
		if link.startswith("http://"):
			return link
		elif link.startswith("//"):
			return "http:"+link 
		
		elif link.startswith('/'):
			full_link = urllib.parse.urljoin(url, link)
			return full_link


def main():
	parser = Parser("")
	

if __name__ == '__main__':
	main()
