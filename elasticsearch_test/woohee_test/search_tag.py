import json
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict
from requests_html import HTMLSession
import urllib.parse as url_parse
import re     

raw_index_name = "raw"
raw_doc_type = "twitter"
index_name = "analysis"
doc_type = "doc"
es = Elasticsearch("http://54.180.87.34:9200")  #localhost = 127.0.0.1:9200


results = es.search(index=index_name, body={'query':{'match':{'author':'한국인터넷진흥원'}}})

for result in results['hits']['hits']:
	print( 'source:', result['_source']['title'])
	#print( 'source:', result['_source']['timestamp'])
	#print("\n")