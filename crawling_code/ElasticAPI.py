from elasticsearch import Elasticsearch
import os 
from collections import OrderedDict
import json


def if __name__ == "__main__":
    elasticsearch_ip = os.getenv('ELASTICSEARCH_HOST','localhost')
    es = Elasticsearch(elasticsearch_ip)

def data_insert(index="raw", doc_type="twitter", body=None, id=None):
    '''
    - raw index
    "mappings": {
        "twitter":{
            "properties": {
                "html":{"type": "text"},
            }
        }
    }

    - analysis index
    "mappings": {
        "doc":{
            "properties": {
                "author": {"type": "text"}, #작성자
                "timestamp": {"type":"date"}, #작성시간 "2015-01-01" or "2015/01/01 12:10:30".
                "title": {"type": "text"},# 제목
                "contents": {"type": "text"}, #글 내용
                "nlp_contents": {"type": "keyword"},# 형태소 분석된 내용
                "url":{"type": "text"},#글 URL
                "publisher": {"type": "keyword"}, #글 출처 출판사(보안뉴스, 트위터 등)
                "tag": {"type": "keyword"},#추후 태그
            }
        }
    }
    '''
    res = es.index(index=index, doc_type=doc_type, body=body, id = id)

#raw data 일 경우
def raw_index_to_json(html_data):
    file_data = OrderedDict()
    #file_data['html'] = ''' <!doctype html><html><head><title>Hello HTML</title></head><body><p>Hello World!</p></body></html>'''
    file_data['html'] = html_data
    body = json.dumps(file_data, ensure_ascii=False, indent="\t")
    return body

#analysis data 일 경우
def analysis_index_to_json(author="홍길동", timestamp="2015-01-01", title="의미 없는 제목",contents="냉무", nlp_contents="형태소", url="http://naver.com", publisher="트위터", tag ="태그 종류"):
    file_data = OrderedDict()
    file_data['author'] = author
    file_data['timestamp'] = timestamp
    file_data['title'] = title
    file_data['contents'] = contents
    file_data['url'] = url
    file_data['publisher'] = publisher
    file_data['tag'] = tag

    body = json.dumps(file_data, ensure_ascii=False, indent="\t")
    return body

# body = analysis_index_to_json(author=None)
# data_insert(index="analysis", doc_type="doc", body=body, id=1)