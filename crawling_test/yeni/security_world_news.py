from requests_html import HTMLSession
import re
#import urllib.parse as url_parse

session = HTMLSession();
r = session.get('https://www.boannews.com/media/view.asp?idx=83776')
#r = session.get('https://t.co/9JUu2eHmG1')

news_content_tag='body > div#wrap > div#body > div#body_left > div#media > div > div#news_content > br'

f = open("security_world_news.txt", "w", encoding='UTF-8')
print(r.text)
#print(r.html)
#Get News Title & Content Summary

#r.html.render()

for line2 in r.html.find('div#news_title02'):
        news_title = line2.text
        print('제목: ', news_title)


for line2 in r.html.find('div#news_util01'):
        date = line2.text
        print('날짜: ', date[8:])


for line2 in r.html.find('div#news_content'):
        content = line2.text
        print('내용: ', content)


for line2 in r.html.find('div#news_content'):
        writer = re.match(r'\[[가-힣\s]*\([a-zA-Z0-9@.]*\)\]',a).group()
        print('작성자: ', writer)

f.close()
