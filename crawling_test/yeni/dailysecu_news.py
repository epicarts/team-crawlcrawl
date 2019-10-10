from requests_html import HTMLSession
import urllib.parse as url_parse

session = HTMLSession();
f = open("dailysecu_news.txt", "w", encoding='UTF-8')
r = session.get('https://www.dailysecu.com/news/articleView.html?idxno=73130')


class DailySecu_Crawler:
    def __init__(self):
        self.Module_Name = "DailySecu Crawler"
        self.Version = 0.1
        
        self.session = HTMLSession();
        self.tag_selector = 'html.whatinput-types-initial > body > div.off-canvas-wrapper > div.off-canvas-wrapper-inner > div.off-canvas-content> div#user-wrap.min-width-1080 > section#user-container.posi-re.text-left.auto-pady-25.float-center.width-1080 > div.float-center.max-width-1080 > div.user-content > section.user-snb > div.user-snb-wrapper > article.article-veiw-body.view-page.font-size17 > div#article-view-content-div > p'
        self.site_url = 'https://www.dailysecu.com/news/articleView.html?idxno=73130'
        
    def Print_Module_Name(self):
        print( self.Module_Name +"\r\n" )

    def run(self, search_str):        
        r = self.session.get( self.site_url)
        r.html.render()
        return r.html.find( self.tag_selector )

        
    
if __name__ == "__main__":
    
    test = DailySecu_Crawler()

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

f.close()






'''
from requests_html import HTMLSession

session = HTMLSession();
r = session.get('https://www.dailysecu.com/news/articleView.html?idxno=73130')

f = open("dailysecu_news.txt", "w", encoding='UTF-8')

#Get News Title & Content Summary
for line in r.html.find('div.article-head-title'):
	print(line.text)
	print("\n")
	f.write(line.text)

f.close()
'''
