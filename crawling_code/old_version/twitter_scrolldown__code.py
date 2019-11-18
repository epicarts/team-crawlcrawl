from requests_html import HTMLSession
from collections import OrderedDict
import re
import os
'''
크로미윰.  스크롤 다운을 통한 데이터 수집 소스코드 
'''
def query_mydb(sql, val=None):
    '''
        sql = "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목ㅅ32323ㄴㅇ22', 'http://google.com')"
    '''
    mysql_ip = os.getenv('MYSQL_HOST','localhost')

    connection = pymysql.connect(
    host=mysql_ip,
    user="root",
    passwd="root",
    database="logstash_db",
    charset='utf8mb4'
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, val) # sql 구문 삽입
            connection.commit()
    finally:
        connection.close()


def news_crawl(r2):
    '''
    보안 뉴스의 데이터를 추출해서 json 형태로 리턴함.
    '''
    for line2 in r2.html.find('div#news_title02'):
        news_title = line2.text
        #print('제목: ', news_title)

    for line2 in r2.html.find('div#news_util01'):
        date = line2.text
        #print('날짜: ', date[8:])

    author = "unknown"
    for line2 in r2.html.find('div#news_content'):
        writer = re.search(r'\[[가-힣\s]*\]',line2.text)
        if(writer != None):
            #print('작성자: ', writer.group())
            author = writer.group()

    for line2 in r2.html.find('div#news_content'):
        content = re.sub(r'\[[가-힣\s]*[=][\sa-zA-Z0-9]*\]', '', line2.text)
        #print('내용: ', content)


    file_data = OrderedDict()
    file_data['author'] = author
    file_data['post_create_datetime'] = date[8:] + ":00" # 2015-01-01 12:10:00
    file_data['title'] = news_title
    file_data['content'] = content
    file_data['url'] = r2.url
    file_data['publisher'] = '보안뉴스'
    return file_data



session = HTMLSession()         #웹 페이지에 접속하기 위해 준비. (일을 시키기 위한 일꾼 준비)
r = session.get('https://twitter.com/boannews') #해당 웹페이지에 접속하여 그 결과를 r 변수에 저장


#pip3 install websockets==6.0 --force-reinstall 소켓 다운그레이드 필요
r.html.render(scrolldown=1000,sleep=0.5)

extract_link = 'body > #doc > #page-outer > #page-container > div > div > div > div > div > div > #timeline > div > div > #stream-items-id > .js-stream-item.stream-item.stream-item > div > div.content > div.js-tweet-text-container > p > a'
extract_url_list = list()

for line in r.html.find(extract_link):
    url = line.text.replace('…','')         #...제거
    url_len = len(url)
    extract_url_list.append(url[:url_len-1])            #공백제거

#보안뉴스 링크가 아닌 링크는 전부 제거.
boannews_urls = [url for url in extract_url_list if "http://www.boannews.com/" in url] 
finish = len(boannews_urls)-1

for num, boannews_url in enumerate(boannews_urls):
    r2 = session.get(boannews_url)
    try:
        json_data = news_crawl(r2)# 수집한 데이터를 입맞대로 가공.
        sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], json_data['post_create_datetime'])
        query_mydb(sql=sql, val=val)
    except:
        print("파싱 또는 SQL 에러")
        pass
    print("current: {} / finish: {} / url: {}".format(num, finish, boannews_url))