from requests_html import HTMLSession
import urllib.parse as url_parse

s_urlenc=url_parse.quote("랜섬웨어")
session = HTMLSession();
r = session.get('https://search.naver.com/search.naver?where=news&query='+s_urlenc)

tag_sel='body > #wrap > #container > #content > #main_pack > div > ul.type01 > li'

#Get News Title
for news_num, news_title in enumerate( r.html.find(tag_sel) ):
	print( "[{}] {}".format(news_num, news_title.text) )
	print("")
