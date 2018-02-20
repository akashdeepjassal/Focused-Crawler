from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []
		

	def handle_starttag(self, tag, attrs):
		if tag.lower() == 'a' and len(attrs) > 0:
			for attr, value in attrs:
				if attr == 'href':
					self.links.append(value)
					


