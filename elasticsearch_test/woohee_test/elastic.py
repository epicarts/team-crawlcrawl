import json
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict
from requests_html import HTMLSession
import urllib.parse as url_parse

index_name = "raw"
doc_type = "twitter"
es = Elasticsearch("http://127.0.0.1:9200/")  #localhost = 127.0.0.1:9200
	
def insert(index_name, doc_type, body = None, id = None):
	insert_data = es.index(index=index_name, doc_type=doc_type, body=body,id=id)
	return insert_data

def raw_index_to_json(html_data):
	raw_data = OrderedDict()
	raw_data['html'] = html_data
	body = json.dumps(raw_data,ensure_ascii=False, indent = 2)
	return body
  
#보안뉴스 기사의 html(r2.text)       

#r.이라는 객체가 얻어온 html 코드를 얻어와서 find()를 사용하여 경로를 지정해줘서 해당 경로에 위치하는 태그 객체를 얻어온다 
#line.links로 얻을 수 있는 보안뉴스 기사 url의 단축url은 크롤링이 안되는 오류가 생겨서
#line.text로 긴 url을 얻어옴. 해당 url의 경우 'https://www.boannews.com/media/view.asp?idx=83776 …' 형태로 크롤링이 되므로
#…을 제거하고 공백을 제거하여 리스트 형 변수 news_url에 넣어줌 

if __name__ == "__main__":

	session = HTMLSession()         #웹 페이지에 접속하기 위해 준비. (일을 시키기 위한 일꾼 준비)
	r = session.get('https://twitter.com/boannews') #해당 웹페이지에 접속하여 그 결과를 r 변수에 저장
	#'보안뉴스'트위터에서 보안뉴스 기사 url이 담긴 부분의 경로
	extract_news_link = 'body > #doc > #page-outer > #page-container > div > div > div > div > div > div > #timeline > div > div > #stream-items-id > .js-stream-item.stream-item.stream-item > div > div.content > div.js-tweet-text-container > p > a'

	#트위터에서 긁어온 보안뉴스 기사 url을 저장할 list형 변수 news_url 선언
	news_url = list()

	#render(): 자바스크립트가 실행된 html 코드를 받아올수 있게 하는 함수
	#트위터는 스크롤을 내리면 계속해서 밑에 내용이 추가되는 형태로 이루어짐
	#코드로 스크롤을 n번 시킴. 스크롤해서 바로 뜨는게 아니라 200ms를 쉬고 나온 html 결과를 가져옴.
	r.html.render(scrolldown=1,sleep=0.2)



	for line in r.html.find(extract_news_link):
		url = line.text.replace('…','')         #...제거
		url_len = len(url)
		news_url.append(url[:url_len-1])            #공백제거



	#news_url에 저장된 트위터에서 읽어온 뉴스url을 r2변수에 저장 및 함수로 보내기
	for url in news_url:
		r2 = session.get(url)
		doc = r2.text
		#print(doc)
		json_data = raw_index_to_json(html_data = doc) # 알맞게 가공
		#print(json_data)
		insert_data = insert(index_name, doc_type, body=json_data)
		
		


	



#es.index(index=index_name, doc_type='string', body=doc1,id=1)