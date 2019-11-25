import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://127.0.0.1:9200/")
print(es.info())
b_body = {
		"mappings": {
            "twitter": {
                "properties": {
                	"HTMI" : {"type": "text"}   //raw_data
				}
			}
		}
	}
def make_index(es, index_name):
    """인덱스를 신규 생성한다(존재하면 삭제 후 생성) """
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    print(es.indices.create(index=index_name))
print('\n')

index_name = 'dictionary'
make_index(es, index_name) # 상품 데이터 덩어리(인덱스)를 생성한다 

with open("/workspace/test/dictionary_data.json",'r',encoding='utf-8') as json_file:
	json_data = json.loads(json_file.read())
	
body = ""
for i in json_data:
	body = body + json.dumps({"index": {"_index":"dictionary","_type": "dictionary_datas"}}) + '\n'
	body = body + json.dumps(i,ensure_ascii=False) + '\n'
	
es.bulk(body)