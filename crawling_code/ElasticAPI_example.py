from collections import OrderedDict
from elasticsearch import Elasticsearch, helpers
import json


class ElasticAPI:
    def __init__(self):  
        elasticsearch_ip = os.getenv('ELASTICSEARCH_HOST','localhost')
        self.es = Elasticsearch(elasticsearch_ip)

    def data_insert(self, index="raw", doc_type="twitter", body=None, id=None):
        res = self.es.index(index=index, doc_type=doc_type, body=body, id = id)
        return res


    def all_index(self):
        res = self.es.cat.indices()
        print(res)
        return res
    
    def get(self,index="raw", id=None):
        res = self.es.get(index=index, id=id)
        return res

    #raw data 일 경우
    def raw_index_to_json(self, html_data):
        file_data = OrderedDict()
        #file_data['html'] = ''' <!doctype html><html><head><title>Hello HTML</title></head><body><p>Hello World!</p></body></html>'''
        file_data['html'] = html_data
        body = json.dumps(file_data, ensure_ascii=False, indent="\t")
        return body

    #analysis data 일 경우
    def analysis_index_to_json(self, author="홍길동", timestamp="2015-01-01", title="의미 없는 제목",contents="냉무", nlp_contents="형태소", url="http://naver.com", publisher="트위터", tag =None):
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


if __name__ == "__main__":
    
    #raw data 를 삽입하는 예제
    ea = ElasticAPI()#클래스 생성
    data = "나는 html 데이터야"
    json_data = ea.raw_index_to_json(html_data=data) # 알맞게 가공
    print(json_data)

    #변환된 json 파일을 엘라스틱 서치에 넣기
    ea.data_insert(index="raw", doc_type="twitter", body=json_data, id=2)

    #넣은거 확인
    res = ea.get(index="raw", id=2)
    print(res)

    #analysis data 를 삽입하느 에제
    ea = ElasticAPI()#클래스 생성
    json_data = ea.analysis_index_to_json(author="길동이", timestamp="2015-01-01", title="의미 없는 제목",contents="냉무", nlp_contents="형태소", url="http://naver.com", publisher="트위터", tag ="태그 종류")
    ea.data_insert(index="analysis", doc_type="doc", body=json_data, id=2)#id 2 삽입
    ea.data_insert(index="analysis", doc_type="doc", body=json_data, id=1)#id 1 삽입


    res = ea.get(index="analysis", id=1)
    print(res)

    ea.all_index()