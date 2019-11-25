'''
from requests_html import HTMLSession
import urllib.parse as url_parse

session = HTMLSession();
r = session.get('https://www.dailysecu.com/news/articleList.html?page=1&total=9798&box_idxno=&sc_section_code=S1N2&view_type=sm')


class DailySecu_list:
    def __init__(self):
        self.Module_Name = "DailySecu List"
        self.Version = 0.1
        
        self.session = HTMLSession()
        #self.tag_selector = 'html.whatinput-types-initial > body > div.off-canvas-wrapper > div.off-canvas-wrapper-inner > div.off-canvas-content> div#user-wrap.min-width-1080 > section#user-container.posi-re.text-left.auto-pady-25.float-center.width-1080 > div.float-center.max-width-1080 > div.user-content > section.user-snb > div.user-snb-wrapper > article.article-veiw-body.view-page.font-size17 > div#article-view-content-div > p'
        self.url_sel = 'html.whatinput-types-initial > body > div.off-canvas-wrapper > div.off-canvas-wrapper-inner > div.off-canvas-content> div#user-wrap.min-width-1080 > section#user-container.posi-re.text-left.auto-pady-25.float-center.width-1080 > div.float-center.max-width-1080 > div.user-content > section.user-snb > article.article-veiw-body > div.article-list > section.article-list-content.type-sm.text-left > div.list-block > div.list-image > a'
        
        self.site_url = 'https://www.dailysecu.com/news/articleList.html?page=1&total=9798&box_idxno=&sc_section_code=S1N2&view_type=sm'
        
    def Print_Module_Name(self):
        print( self.Module_Name +"\r\n" )
        
    def run(self, search_str):        
        r = self.session.get( self.site_url)
        r.html.render()
        return r.html.find( self.tag_selector )
    
    def findurl(self,search_str):
        r = self.session.get(self.site_url)
        r.html.render()
        return r.html.find(self.url_sel)


class DailySecu_Crawl:
    def __init__(self):
        self.Module_Name = "DailySecu Crawler"
        self.Version = 0.1

        self.session = HTMLSession();

    def start(self, news_url):
        self.url = news_url
        print(self.url)

        #r2 = session.get(news_url)
        #r2.html.render()

    def title(self,news_url):
        r2 = session.get(news_url)
        print(r2.html.find('div.article-head-title')


if __name__ == '__main__':
    
    test = DailySecu_list()
    test2 = DailySecu_Crawl()

    raw_url = test.findurl("")

    for line in raw_url:
        news_url = 'https://dailysecu.com'+line.attrs['href']

        url = test2.start(news_url)
        title = test2.title(news_url)
    '''
    '''
    #제목
    for line in r.html.find('div.article-head-title'):
        print(line.text)
        print("")
        f.write(line.text)


    retn_data = test.run("")

    #본문
    f.write("\n")
    for line in retn_data:
        print(line.text)
        f.write(line.text)
    '''




import datetime as dt

import re
from requests_html import HTMLSession
import urllib.parse as url_parse

import os

from collections import OrderedDict
import json

import pymysql


content_sel = 'html.whatinput-types-initial.whatinput-types-keyboard > body > div.off-canvas-wrapper > div.off-canvas-wrapper-inner > div.off-canvas-content> div#user-wrap.min-width-1080 > section#user-container.posi-re.text-left.auto-pady-25.float-center.width-1080 > div.float-center.max-width-1080 > div.user-content > section.user-snb > div.user-snb-wrapper > article.article-veiw-body.view-page.font-size17 > div#article-view-content-div > p'

#웹페이지의 데이터를 추출해서 json 형태로 리턴함.
def dailysecu_crawl(r2):

    url = r2.url
    print('url: ', url)
    
    for line2 in r2.html.find('div.article-head-title'):
        news_title = line2.text
        print('제목: ', news_title)

        
    for line2 in r2.html.find('div.info-text'):
        usr_date = line2.text

    count = 0
    for index in usr_date:
        if index == '승':
            break
        else:
            count = count+1

    author = usr_date[:count-1]
    print('작성자: ', author)

    date = usr_date[count+3:]       #+:00 필요
    print('날짜: ', date)

    publisher = 'DailySecu'
    print('출처: ', publisher)

    
    r2.html.render()
    
    for line2 in r2.html.find(content_sel):
       print(line2.text)
    
    

if __name__ == '__main__':
    session = HTMLSession()
    dailysecu_url = 'https://www.dailysecu.com/news/articleList.html?page=1&total=9798&box_idxno=&sc_section_code=S1N2&view_type=sm'
    url_sel = 'html.whatinput-types-initial > body > div.off-canvas-wrapper > div.off-canvas-wrapper-inner > div.off-canvas-content> div#user-wrap.min-width-1080 > section#user-container.posi-re.text-left.auto-pady-25.float-center.width-1080 > div.float-center.max-width-1080 > div.user-content > section.user-snb > article.article-veiw-body > div.article-list > section.article-list-content.type-sm.text-left > div.list-block > div.list-image > a'
    r = session.get(dailysecu_url)
    r.html.render()

    for line in r.html.find(url_sel):
        news_url = 'https://dailysecu.com'+line.attrs['href']
        #print(news_url)
        
        session2 = HTMLSession()
        r2 = session2.get(news_url)
        #r2.html.render()
        dailysecu_crawl(r2)

