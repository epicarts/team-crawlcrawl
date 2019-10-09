from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch("http://127.0.0.1:9200/")
print(es.info())#정보 표시


doc = {
    'author': 'kimchy',#소유자 kimchy
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),#현재 시간
}

res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
print(res['result'])#created 라고 생김

res = es.get(index="test-index", id=1)
print(res['_source'])
res

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


es.indices.create(index='test-index', ignore=400)

es.indices.create(index='test-index')

es.indices.delete(index='test-index') # 삭제 할 수 없을떄 에러 뱉어냄
es.indices.delete(index='test-index', ignore=[400, 404])

es.search(index="test-index")
es.search(index='test-index', filter_path=['hits.hits._id', 'hits.hits._type'])
es.search(index='test-index', filter_path=['hits.hits._*'])

es.search(index="한국금거래")
