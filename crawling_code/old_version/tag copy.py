import json
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict
from requests_html import HTMLSession
import urllib.parse as url_parse
import re                               #re라는 정규표현식 모듈을 불러와서 사용
import os

raw_index_name = "raw"
raw_doc_type = "twitter"
index_name = "analysis"
doc_type = "doc"


elasticsearch_ip = os.getenv('ELASTICSEARCH_HOST','localhost')
elasticsearch_port = os.getenv('ELASTICSEARCH_PORT','9200')
es = Elasticsearch(elasticsearch_ip)
#es = Elasticsearch("http://127.0.0.1:9200/")  #localhost = 127.0.0.1:9200

def raw_insert(raw_index_name, raw_doc_type, body = None, id = None):
	'''
	기존 함수 파라미터 값과 es.index 파라미터 값이 다름.
	index_name => raw_index_name
	doc_type => raw_doc_type
	'''
	insert_data = es.index(index=raw_index_name, doc_type=raw_doc_type, body=body,id=id)
	return insert_data

def analysis_insert(index_name = index_name, doc_type = doc_type, body = None, id = None):
	insert_data = es.index(index=index_name, doc_type=doc_type, body=body,id=id)
	return insert_data

def raw_index_to_json(html_data):
	raw_data = OrderedDict()
	raw_data['html'] = html_data
	body = json.dumps(raw_data, ensure_ascii=False, indent = 2)
	return body

def analysis_index_to_json(author, timestamp, title, contents, nlp_contents, url, publisher, tag):
	file_data = OrderedDict()
	file_data['author'] = author
	file_data['timestamp'] = timestamp
	file_data['title'] = title
	file_data['contents'] = contents
	file_data['nlp_contents'] = contents
	file_data['url'] = url
	file_data['publisher'] = publisher
	file_data['tag'] = tag

	body = json.dumps(file_data, ensure_ascii=False, indent=2)
	return body

def news_crawl(r2):
	raw_data = r2.text #보안뉴스 기사의 html
	json_data = raw_index_to_json(html_data = raw_data) #알맞게 가공

	'''
	json_data에 담겨 있는 데이터는 원시데이터 (HTML 데이터)

	1. raw_insert 는 raw 인덱스를 넣는 함수.  
	2. index_name 변수 안에는 analysis 라는 값이 들어 있음. 
	3. 수정: raw_index_name 변수로 변경함. raw라는 값이 들어있음.
	4. 수정: doc_type => raw_doc_type
	'''
	raw_insert_data = raw_insert(raw_index_name, raw_doc_type, body=json_data)   #raw_data
    
	url_twitter = r2.url                 #보안뉴스 기사의 url

    #제목, 날짜, 내용, 작성자 별로 크롤링 하여 변수 저장 및 출력
	for line2 in r2.html.find('div#news_title02'):
		news_title = line2.text
		#print('제목: ', news_title)

	for line2 in r2.html.find('div#news_util01'):
		date = line2.text
		#print('날짜: ', date[8:])
	
	for line2 in r2.html.find('div#news_content'):
		writer = re.search(r'\[[가-힣\s]*\]',line2.text)
		if(writer != None):
			print('작성자: ', writer.group())
			#twitter_writer = writer.group()

	origin = '보안뉴스'
	print('출처: ',origin)
    
	for line2 in r2.html.find('div#news_content'):
		content = re.sub(r'\[[가-힣\s]*[=][\sa-zA-Z0-9]*\]', '', line2.text )
		print('내용: ', content)
		
	global twitter_tag
	for line2 in r.html.find('div#news_tag_txt'):
		twitter_tag = line2.text
		print('태그: ', twitter_tag)
		print("ddddddddddddddddddddddddddddd")

	#크롤링한 데이터를 json형태로... 아마 여기서 뻑나는듯... 

	'''
	수정: writer => writer.group()
	writer 는 _sre.SRE_Match object 객체라 문자열이 아니라서 그런듯..

	엘라스틱 timestamp 에는 들어가는 형식이 존재함
	date[8:] 에는 2019-10-26 15:47 이런 데이터가 들어 있음.

	현재 우리가 입력 가능한 포맷은 
	1. 2015-01-01 12:10:30 
	2. 2015-01-01 
	이렇게 두가지로 설정 해 놓음. 원하면 다른것도 추가 가능!

	'''
	tag_json_data = analysis_index_to_json(author = writer.group(), timestamp = date[8:], title = news_title, contents = content, nlp_contents = "None", url = url_twitter, publisher = "트위터", tag = "태그")
	print(tag_json_data)

	insert_tag_data = analysis_insert(index_name = index_name, doc_type = doc_type, body=tag_json_data)

if __name__ == "__main__":

	session = HTMLSession()         #웹 페이지에 접속하기 위해 준비. (일을 시키기 위한 일꾼 준비)
	r = session.get('https://twitter.com/boannews') #해당 웹페이지에 접속하여 그 결과를 r 변수에 저장
#'보안뉴스'트위터에서 보안뉴스 기사 url이 담긴 부분의 경로
	extract_news_link = 'body > #doc > #page-outer > #page-container > div > div > div > div > div > div > #timeline > div > div > #stream-items-id > .js-stream-item.stream-item.stream-item > div > div.content > div.js-tweet-text-container > p > a'
	#트위터에서 긁어온 보안뉴스 기사 url을 저장할 list형 변수 news_url 선언
	news_url = list()	
	
	r.html.render(scrolldown=1,sleep=0.2)
	
	
	for line in r.html.find(extract_news_link):
		url = line.text.replace('…','')         #...제거
		url_len = len(url)
		news_url.append(url[:url_len-1])            #공백제거

	#news_url에 저장된 트위터에서 읽어온 뉴스url을 r2변수에 저장 및 함수로 보내기
	for url in news_url:
		r2 = session.get(url)
		news_crawl(r2)
		print("끝====================================")		