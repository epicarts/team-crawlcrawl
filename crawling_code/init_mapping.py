from elasticsearch import Elasticsearch, helpers
import os 

elasticsearch_ip = os.getenv('ELASTICSEARCH_HOST','localhost')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT','9200')

es = Elasticsearch(elasticsearch_ip)

def create_analysis_index():
    #https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori-tokenizer.html
    body = {
        "settings" : { # 색인(index) 정의 
            "number_of_shards" : 2, # 샤드 개수
            "number_of_replicas": 1, # 레플리카 개수
            "index": { # 색인 전체 설정
                "analysis": {
                    "analyzer": {
                        "nori_analyzer": {# 사용자 정의 분석기
                            "type": "custom",
                            "tokenizer": "nori_user_dict",# 토크나이저 설정
                            "filter": ["my_posfilter"]
                        }
                    },
                    "tokenizer": {
                        "nori_user_dict": {# 토크나이저 정의
                            "type": "nori_tokenizer",# 한글 분석기 (nori)
                            "decompound_mode": "mixed", #토큰을 처리하는 방법, 분해하지 않는다(none), 분해하고 원본삭제(discard), 분해하고 원본 유지(mixed)
                            "user_dictionary": "userdict_ko.txt"
                        }
                    },
                    "filter": {
                        "my_posfilter": { #제거 할 불용어들
                            "type": "nori_part_of_speech",
                            "stoptags": ["E", "IC","J","MAG", "MAJ", "MM",
                            "SP", "SSC", "SSO", "SC", "SE",
                            "XPN", "XSA", "XSN", "XSV",
                            "UNA", "NA", "VSV"]
                        }
                    }
                }
            }
        },
        "mappings": {
            "doc":{
                "properties": {
                    "author": {"type": "text"}, #작성자
                    "post_create_datetime": {"type":"date"},#글 작성시간
                    "title": {"type": "text", "analyzer": "nori_analyzer"},# 제목
                    "content": {"type": "text", "analyzer": "nori_analyzer"}, #글 내용
                    "url":{"type": "text", "index": "false"},#글 URL
                    "publisher": {"type": "keyword"}, #글 출처 출판사(보안뉴스, 트위터 등)
                    "tag": {"type": "keyword"},#태그
                }
            }
        }
    }
    res = es.indices.create(index = "analysis", body = body, include_type_name =True, ignore=[400, 404])
    return res

try:
    create_analysis_index()
    print("Success, Elasticsearch mapping")
except:
    print("Error, Ealsticsearch mapping")
    pass