# web-crawler-python
Description
This Python project implements a recursive web crawler that starts from a root URL, visits all internal links, and continues to explore links found on each visited page. The result is a comprehensive map of how pages within a website are interconnected, ideal for analyzing site structure and link flow.

Core Functionality:
   Recursive Crawling: Begins at a base URL and follows internal links found on each page, visiting them in breadth-first order.
	Link Harvesting: On every visited page, it extracts all internal hyperlinks and queues them for further crawling.
	Cycle Detection: Avoids revisiting pages by maintaining a set of already visited URLs.
	Graph Construction: Builds a directed graph where:Nodes represent individual web pages Edges represent hyperlinks from one page to another
	Visualization: Optionally renders the graph using libraries like networkx and matplotlib to show the site's internal link structure.

Technologies Used:
o	selenium for HTTP requests and HTML parsing
o	urllib.parse for URL normalization and domain filtering
o	re for completion of domain name
o	networkx for graph modeling
o	matplotlib or Plotly for visual output
