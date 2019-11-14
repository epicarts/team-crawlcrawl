from requests_html import HTMLSession

session = HTMLSession();
r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')

#Get News Title
for news_num, news_title in enumerate( r.html.find('.news_txt') ):
	print( "[{}] {}".format(news_num, news_title.text) )
	print("")
