from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pprint as ppr
import json


# 일레스틱서치 IP주소와 포트(기본:9200)로 연결한다
es = Elasticsearch("http://127.0.0.1:9200/") # 환경에 맞게 바꿀 것
es.info()
#print(es.info())
#print('\n')

# 인덱스는 독립된 파일 집합으로 관리되는 데이터 덩어리이다
def make_index(es, index_name):
    """인덱스를 신규 생성한다(존재하면 삭제 후 생성) """
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
   # print(es.indices.create(index=index_name))

index_name = 'goods'
make_index(es, index_name) # 상품 데이터 덩어리(인덱스)를 생성한다 

# 데이터를 저장한다
doc1 = {'goods_name': '삼성 노트북 9',    'price': 1000000,'take': 'on'}
doc2 = {'goods_name': '엘지 노트북 그램', 'price': 2000000,'take': 'off'}
doc3 = {'goods_name': '애플 맥북 프로',   'price': 3000000,'take': 'on'}
es.index(index=index_name, doc_type='string', body=doc1,id=1)
es.index(index=index_name, doc_type='string', body=doc2,id=2)
es.index(index=index_name, doc_type='string', body=doc3,id=3)

es.indices.refresh(index=index_name)


# 상품명에 '노트북'을 검색한다
index = input("검색할 이름:")
results = es.search(index=index_name, body={'query':{'match':{'goods_name':index}}})
#print('\n')
ppr.pprint(results)
#hits : 응답 데이터 정보 (* 검색결과 데이터는 hits > hits > _source 안에 데이터가 있다.)
for result in results['hits']['hits']:
    print( 'source:', result['_source']['goods_name'])
print('\n')
#조회
#doc = es.get(index = index_name,doc_type = 'string',id=1)
#print(doc)
#print json.dumps(doc, indent = 2)

