from elasticsearch import Elasticsearch, helpers
import os 

elasticsearch_ip = os.getenv('ELASTICSEARCH_HOST','localhost')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT','9200')

es = Elasticsearch(elasticsearch_ip)

def create_raw_index():
    #인덱스 생성
    #raw/twitter/
    body = {
        "mappings": {
            "twitter":{
                "properties": {
                    "html":{"type": "text"},
                }
            }
        }
    }
    res = es.indices.create(index = "raw", body = body, include_type_name =True, ignore=[400, 404])
    return res

def create_analysis_index():
    body = {
        "mappings": {
            "doc":{
                "properties": {
                    "author": {"type": "text"}, #작성자
                    "timestamp": {"type":"date", "format":"yyyy-MM-dd||yyyy-MM-dd HH:mm"}, #작성시간 "2015-01-01" or "2015-01-01 12:10:30".
                    "title": {"type": "text"},# 제목
                    "contents": {"type": "text"}, #글 내용
                    "nlp_contents": {"type": "keyword"},# 형태소 분석된 내용
                    "url":{"type": "text"},#글 URL
                    "publisher": {"type": "keyword"}, #글 출처 출판사(보안뉴스, 트위터 등)
                    "tag": {"type": "keyword"},#추후 태그
                }
            }
        }
    }
    res = es.indices.create(index = "analysis", body = body, include_type_name =True, ignore=[400, 404])
    return res

create_raw_index()
create_analysis_index()