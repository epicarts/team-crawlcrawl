import datetime as dt

import re
from requests_html import HTMLSession

import os

from collections import OrderedDict
import json

import pymysql

content_sel = 'body > div#wrap > div#contentWrap > div.widthWrap > div#contentDiv.contents > table.basicView > tbody > tr > td.cont'


def query_mydb(sql, val=None):
    '''
        sql = "INSERT INTO raw_table (title, URL) VALUES('뉴스 제목', 'http://google.com')"
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


def select_mydb(sql, val=None):
    '''
        sql = "SELECT * FROM raw_table WHERE id=5"
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
            result = cursor.fetchall()
    finally:
        connection.close()

    return result


#보안 뉴스 웹페이지의 데이터를 추출해서 json 형태로 리턴함.
def kisa_crawl(r2):

    url = r2.url
    #print('url: ', url)

    for line2 in r2.html.find('th.bg_tht'):
        raw = line2.text

    news_title = raw[:len(raw)-10]
    #print('제목: ', news_title)
    
    date = raw[len(raw)-10:]
    #print('날짜: ', date)


    for line2 in r2.html.find(content_sel):
        content = line2.text
        #print('내용: ', content)

    author = 'KISA'
    #print('작성자: ', author)

    publisher = 'KISA'
    #print('출처: ', publisher)

    file_data = OrderedDict()
    file_data['author'] = author
    file_data['post_create_datetime'] = date + "00:00:00" # 2015-01-01 12:10:00
    file_data['title'] = news_title
    file_data['content'] = content
    file_data['url'] = r2.url
    file_data['publisher'] = publisher
    return file_data

if __name__ == '__main__':
    session = HTMLSession()
    kisa_url = 'https://www.krcert.or.kr/data/trendList.do?page=1&sort_code=&search_sort=title_name&search_word='
  
    r = session.get(kisa_url)# 세션 열고 수집   

    for line in r.html.find('td.colTit'):
        raw_url = str(line.links)
        news_url = 'https://www.krcert.or.kr'+raw_url[2:len(raw_url)-2]
        #print('news_url:', news_url)


        #SQL에서 URL 중복 체크
        sql = "select EXISTS (select * from raw_table WHERE url=%s) as success"
        val = (news_url)
        is_exists = select_mydb(sql, val)[0][0] # ture: 1 / false: 0 반환

        if is_exists: # 해당 URL이 있으면 패스 
            continue
            #print("Already Exists url")
        else:# 해당 URL이 없으면 크롤링 후 삽입하기.
            session = HTMLSession()
            r2 = session.get(news_url)  # 세션 열고 수집.
            

            #try except, 중간에 파싱결과 오류나면 pass하고 다음거..
            try:
                json_data = kisa_crawl(r2)# 수집한 데이터를 입맞대로 가공.
                        #sql query문으로 삽입
                #print('1')
                sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], json_data['post_create_datetime'])
                query_mydb(sql=sql, val=val)
            except:
                print("예외 발생.")
                pass
    print("보안뉴스 웹사이트 수집 완료")

