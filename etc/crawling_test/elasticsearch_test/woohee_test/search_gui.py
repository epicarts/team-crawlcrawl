import json
from elasticsearch import Elasticsearch, helpers
from collections import OrderedDict
import urllib.parse as url_parse
import re     

from tkinter import *
from tkinter import ttk

index_name = "analysis"
doc_type = "doc"

es = Elasticsearch("http://crawlcrawl.com:9200")

def content_print():
    print ("content select")
    search_content = E1.get()
    print(search_content)
    
    results = es.search(index="analysis", body={'query':{'match':{'content':search_content}}})
    #hits : 응답 데이터 정보 (* 검색결과 데이터는 hits > hits > _source 안에 데이터가 있다.)
    for result in results['hits']['hits']:
        print('id:', result['_id'])
        print('content:', result['_source']['content'])
        print('\n')
        
def title_print():
    print ("title select")
    search_title = E1.get()
    print(search_title)
    results = es.search(index="analysis", body={'query':{'match':{'title':search_title}}})
    for result in results['hits']['hits']:
        print('id:', result['_id'])
        print('title:', result['_source']['title'])
        print('\n')
    
def author_print():
    print ("author select")
    search_author = E1.get()
    print(search_author)
    results = es.search(index="analysis", body={'query':{'match':{'author':search_author}}})
    #results = es.search(index="analysis", body={'query':{'match':{'author':'[보안뉴스 원병철 기자]'}}})
    for result in results['hits']['hits']:
        print('id:', result['_id'])
        print( 'source:', result['_source']['author'])
        print('\n')

def publisher_print():
    print ("publisher select")
    search_publisher = E1.get()
    print(search_publisher)
    
    results = es.search(index="analysis", body={'query':{'match':{'publisher':search_publisher}}})
    for result in results['hits']['hits']:
        print('id:', result['_id'])
        print('publisher:', result['_source']['publisher'])
        print('\n')

if __name__ == "__main__":
	
	root = Tk()   #하나의 컨테이너(창) 생성
	root.geometry("600x200")    #크기 설정
	root.title("Elasticsearch_search")  #제목
	
	frame1=Frame(root,background='gray')
	frame1.pack(fill=BOTH,ipadx=10, ipady=10,side=TOP)
	
	root_Label=Label(text='Elasticsearch 검색창에 오신 것을 환영합니다~~~',background='gray',foreground='white',font=("돋움",15,'bold'))
	root_Label.pack(fill=BOTH) #pack()해줘야 보인다.
	
	frame2=Frame(root,background='gray')
	frame2.pack(fill=BOTH,ipadx=10, ipady=10,side=TOP)
	
	frame3=Frame(root,background='white')
	frame3.pack(fill=BOTH,ipadx=0.5, ipady=0.5,side=TOP)

	frame4=Frame(root,background='gray')
	frame4.pack(fill=BOTH,ipadx=5, ipady=5,side=TOP)

	frame5=Frame(root,background='gray')
	frame5.pack(fill=BOTH,ipadx=70, ipady=70,side=LEFT)

	frame6=Frame(root,background='gray')
	frame6.pack(fill=BOTH,ipadx=10, ipady=10,side=LEFT)
	
	frame7=Frame(root,background='gray')	
	frame7.pack(fill=BOTH,ipadx=10, ipady=10,side=LEFT)
	
	frame8=Frame(root,background='gray')
	frame8.pack(fill=BOTH,expand=1)
	
	E1=Entry(frame6)
    #E1.insert(10,'')
	E1.grid(row=1,column=0)
	
	button1 = Button(frame7,text='      내용      ',command=content_print)
	button1.grid(row=1,column=0)
	button2 = Button(frame7,text='      제목      ',command=title_print)
	button2.grid(row=2,column=0)
	button3 = Button(frame7,text='     작성자    ',command=author_print)
	button3.grid(row=3,column=0)
	button4 = Button(frame7,text='     출판사    ',command=publisher_print)
	button4.grid(row=4,column=0)
	
	root.mainloop() #root를 무한 루프



''' 참고 링크
    https://blog.naver.com/yheekeun/220701055744
    https://blog.naver.com/yheekeun/220702835752
    https://neverendinglearning.tistory.com/m/29
'''
