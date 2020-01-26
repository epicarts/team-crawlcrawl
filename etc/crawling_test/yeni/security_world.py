from requests_html import HTMLSession

session = HTMLSession();
r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')
tag_sel='body > div#wrap > div#body > div#body_top > div#news_title02'

f = open("security_world_news.txt", "w", encoding='UTF-8')

#Get News Title & Content Summary
for line in r.html.find('#news_title02'):
	print(line.text)
	print("\n")
	f.write(line.text)

for line in r.html.find('#news_content'):
	print(line.text)
	print("\n")
	f.write(line.text)

f.close()
