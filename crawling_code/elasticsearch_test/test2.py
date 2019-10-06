from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch("http://127.0.0.1:9200/")
print(es.info())
helpers.bulk()
helpers.scan()

