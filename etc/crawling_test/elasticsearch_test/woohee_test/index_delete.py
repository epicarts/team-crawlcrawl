from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pprint as ppr
import json

# 일레스틱서치 IP주소와 포트(기본:9200)로 연결한다
es = Elasticsearch("http://127.0.0.1:9200/") # 환경에 맞게 바꿀 것
#es.info()
#print(es.info())
#print('\n')

# 인덱스는 독립된 파일 집합으로 관리되는 데이터 덩어리이다
index_name = 'analysis'
es.indices.delete(index=index_name)
   # print(es.indices.create(index=index_name))


