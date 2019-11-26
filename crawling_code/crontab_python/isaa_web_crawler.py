import datetime as dt

import re
from requests_html import HTMLSession
import urllib.parse as url_parse

import os

from collections import OrderedDict
import json

import pymysql

date_sel = 'html > body > div#wrapper > div#container > div#content > div#con_area > table.board_Vtable > thead > tr > td > ul > li'
from_sel = 'html > body > div#wrapper > div#container > div#content > div#con_area > table.board_Vtable > tbody > tr > td > div.board_content > p > a > span'

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



#웹페이지의 데이터를 추출해서 json 형태로 리턴함.
def isaa_crawl(r2):

    for line2 in r2.html.find('th'):
        raw_title = line2.text
        

    flag = 0
    for index in raw_title:
        if index == ' ':
            break
        else:
            flag = flag + 1

    news_title = raw_title[flag+1:]
    print('제목: ', news_title)
    

    for line2 in r2.html.find(date_sel):
        if len(line2.text)>10:
            date = line2.text
            print('날짜: ', date)

    for line2 in r2.html.find('div.board_content'):
        content = line2.text
        print("내용: ", content)
        
    
    #author = "unknown"
    for line2 in r2.html.find('div.board_content'):
        writer = re.search(r'\[[가-힣\s]*\]',line2.text)
        if(writer != None):
            print('작성자: ', writer.group())
            author = writer.group()

    #원문 url
    for line2 in r2.html.find(from_sel):
        if len(line2.text)>20:
            raw_url = line2.text
            re_url = line2.text
            print('원문 url: ', raw_url)


    publisher = 'ISAA'
    print('출처: ', publisher)

    file_data = OrderedDict()
    file_data['author'] = author
    file_data['post_create_datetime'] = date # 2015-01-01 12:10:00
    file_data['title'] = news_title
    file_data['content'] = content
    file_data['url'] = r2.url
    file_data['publisher'] = publisher
    return file_data

if __name__ == '__main__':
    session = HTMLSession()
    isaa_url = 'http://isaa.re.kr/index.php?pg=1&page=list&hCode=BOARD&bo_idx=4&sfl=&stx='
    url_sel = 'body > div#wrapper > div#container > div#content > div#con_area > div#con_area > form > table.board_table > tbody > tr > td.alignLeft> a'
    
    r = session.get(isaa_url)   #세션 열고 수집  

    for line in r.html.find(url_sel):
        news_url = 'http://isaa.re.kr/index.php'+line.attrs['href']
        #print('new_url:', news_url)

        #SQL에서 URL 중복 체크
        sql = "select EXISTS (select * from raw_table WHERE url=%s) as success"
        val = (news_url)
        is_exists = select_mydb(sql, val)[0][0] # ture: 1 / false: 0 반환

        if is_exists: # 해당 URL이 있으면 패스 
            continue
            print("중복중복!")
            
        else:# 해당 URL이 없으면 크롤링 후 삽입하기.
            session = HTMLSession()
            r2 = session.get(news_url)  # 세션 열고 수집.
            

            #try except, 중간에 파싱결과 오류나면 pass하고 다음거..
            try:
                json_data = isaa_crawl(r2)# 수집한 데이터를 입맞대로 가공.
                
                        #sql query문으로 삽입
                sql = "INSERT INTO raw_table (title, author, content, url, publisher, post_create_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
                print('2')
                val = (json_data['title'], json_data['author'], json_data['content'], json_data['url'], json_data['publisher'], json_data['post_create_datetime'])
                print('3')
                query_mydb(sql=sql, val=val)
                print('4')
            except:
                print("예외 발생.")
                pass
    print("ISAA 웹사이트 수집 완료")

