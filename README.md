# Focused Crawler
pip install -r requirements.txt

# Introduction
This is a primitive focused crawler in Python that attempts to crawl web pages on a particular topic. Given a query(a set of keywords) and a number **_n_** provided by a user, the crawler would contact a Google search engine API and get the top-10 results for this query, called the **starting pages**. Then the crawl from the starting pages using a **focused strategy** until a total of n pages being collected, with most of these pages being relevant to the query/topic. Each page would be crawled only once, and stored in a file.
##How to run
Run the crawler.py file in the terminal, type in three parameters following the prompts. 

>Enter search query: 

>Set total number of webpages to be crawled: 

>Set limits on how many webpages be crawled from single site: 

The first one “Enter search query: ” is the query you want to search. The second one is the total number of webpages you want to crawled. The third one is setting a limit for each website to avoid crawling too much webpages from single site. 
##Output
The crawler would output a list of all visited URLs, in the order they are visited, into a file, together with such information such as the size of each page, the depth of each page (distance from the start pages), and whether the page was relevant.
