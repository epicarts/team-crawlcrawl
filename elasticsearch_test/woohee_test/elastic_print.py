import json
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict
from requests_html import HTMLSession
import urllib.parse as url_parse

index_name = "raw"
doc_type = "twitter"
es = Elasticsearch("http://127.0.0.1:9200/")  #localhost = 127.0.0.1:9200

get_data = es.get(index = index_name, doc_type = doc_type,id = 1)
print(get_data['_source'])