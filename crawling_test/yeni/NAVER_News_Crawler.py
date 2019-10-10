from requests_html import HTMLSession
import urllib.parse as url_parse

class NaverNews_Crawler:
	def init(self):
		self.Module_Name = "NaverNews Crawler"
		self.Version = 0.1

		self.session = HTMLSession();
    self.tag_selector = 'body > #wrap > #container > #content > #main_pack > div > ul.type01 > li'
    self.site_url = '<https://search.naver.com/search.naver?where=news&query=>'
    
	def Print_Module_Name(self):
    print( self.Module_Name +"\\r\\n" )

	def run(self, search_str):
    tmp=url_parse.quote( str(search_str) )      
    
    r = self.session.get( self.site_url + tmp )
    
    return r.html.find( self.tag_selector )