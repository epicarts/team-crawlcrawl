from requests_html import HTMLSession
import urllib.parse as url_parse

session = HTMLSession();
r = session.get('https://www.boannews.com/media/view.asp?idx=83662&page=1&mkind=&kind=1&skind=5&search=title&find=')
tag_sel='body > div#wrap > div#body > div#body_top'

f = open("security_world_news.txt", "w", encoding='UTF-8')
#print(r.html)
#Get News Title & Content Summary
for line in r.html.find(tag_sel):
	print(line.text)
	print("\n")
	f.write(line.text)

'''

f.close()
