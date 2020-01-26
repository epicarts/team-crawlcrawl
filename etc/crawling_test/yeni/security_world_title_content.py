from requests_html import HTMLSession

session = HTMLSession();
r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')

f = open("security_world_title_content_data.txt", "w", encoding='UTF-8')
print(r.html)

#Get News Title & Content Summary
for line in r.html.find('.news_list'):
	print(line.text)
	print("")
	f.write(line.text)
	

f.close()
