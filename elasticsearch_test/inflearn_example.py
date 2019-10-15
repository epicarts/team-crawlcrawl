from elasticsearch import Elasticsearch, helpers

import json
'''
인프런 따라해보기
'''
es.cat.indices()#엘라스틱 서치에 있는 모든 인덱스 조회하기
es = Elasticsearch("http://127.0.0.1:9200/")


'''
만약 API 지원이 안된다면..?
'''
#curl -XPUT http://localhost:9200/bank_en_ver1/account/new_id2?pretty -d
'''
{
    "state": "NY"
}
'
{
  "_index" : "bank_en_ver1",
  "_type" : "account",
  "_id" : "new_id2",
  "_version" : 1,
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "created" : true
}
'''
res = es.transport.perform_request(method = 'PUT',
                                    url = '/classes/class/4',
                                    body = {
                                            'state': 'NY'
                                    })

res
if ret_code == 200: # http 응답 코드만 확인
    print "OK"



es.indices.get(index='classes', ignore=[400, 404])# 그냥 가져오면 오류

es.indices.create(index="classes")#인덱스 만들기
es.indices.get(index="classes")

es.indices.delete(index="classes")
es.indices.get(index='classes', ignore=[400, 404])# 지웟으니 오류

#POST http://localhost:9200/classes/class/1 -d    인덱스/타입/id body값
body = {
    "title": "Algorithm",
    "professor":"John"
}
es.index(index="classes", doc_type="class", id=1, body=body)

#GET http://localhost:9200/classes/class/1    인덱스/타입/id body값
res = es.get(index="classes", id=1)
print(json.dumps(res, indent=2))# 이쁘게 출력 가능

#json 파일 불러와서 저장하기
import os
print(os.getcwd())
with open('D:\\github\\team-crawlcrawl\\crawling_code\\elasticsearch_test\\oneclass.json') as data_file:
    data = json.load(data_file)
es.index(index="classes", doc_type="class", id=1, body=data)
res = es.get(index="classes", id=1)
print(json.dumps(res, indent=2))# 이쁘게 출력 가능

'''
데이터 업데이트
'''

es.index(index="classes", doc_type="class", id=1, body=body)
res = es.get(index="classes", id=1)
print(json.dumps(res, indent=2))# 이쁘게 출력 가능

#필드를 추가시킴 _source
update_field = {
    "doc" : {"unit": 1}
}
update_field
#POST http://localhost:9200/classes/class/1/_update -d
es.update(index="classes", doc_type="class", id=1, body=update_field)
res = es.get(index="classes", id=1)
print(json.dumps(res, indent=2))# 이쁘게 출력 가능

#스크립트도 사용가능 unit 만 5 증가시키자
update_field = {"script" : "ctx._source.unit += 5"}
#POST http://localhost:9200/classes/class/1/_update -d
es.update(index="classes", doc_type="class", id=1, body=update_field)
res = es.get(index="classes", id=1)
print(json.dumps(res, indent=2))# 이쁘게 출력 가능



'''
bulk 벌크 사용하기
두개의 라인으로 구성이 되어 있음.
{ "index" : { "_index" : "classes", "_type" : "class", "_id" : "1" } }
- 메타데이터: 어떤 인덱스에 type 에 id는 무엇이다 라는 명령어

{"title" : "Machine Learning","Professor" : "Minsuk Heo","major" : "Computer Science","semester" : ["spring", "fall"],"student_count" : 100,"unit" : 3,"rating" : 5, "submit_date" : "2016-01-02", "school_location" : {"lat" : 36.00, "lon" : -120.00}}
- 실제 저장 되어 있음.
'''
#http://localhost
path = 'D:\\github\\team-crawlcrawl\\crawling_code\\elasticsearch_test\\classes.json'
es.bulk(index="classes", )

import codecs

classes_data = codecs.open(path, "r", "utf-8")
data = classes_data.read()
classes_data.close()
res=es.bulk(body=data)
print(json.dumps(res, indent=3, separators=(',', ': ')))

res
#bulk 불러오기
res = es.get(index="classes",doc_type="class", id=5)
res

res = es.transport.perform_request(method = 'GET' ,url = '/classes/_mapping')
print(json.dumps(res, indent=3, separators=(',', ': ')))
