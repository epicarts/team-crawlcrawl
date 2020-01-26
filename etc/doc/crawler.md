# Crawler 사용 정보 수집 모듈
* requests-html 모듈을 사용한 크롤러 제작

  기존 Python Crawler 소스들을 보면 requests, urllib 등의 모델을 사용하여 크롤링을 수행한다. 하지만 이 모듈들의 단점은 javascript가 실행되지 않은 상태의 html 코드만 가져와 javascript를 사용하여 html 코드가 변경되게 만든 페이지의 경우 크롤링이 불가능 하다는 단점이 있다. (AJAX로 요청을 해서 얻어오기 전까지 페이지에 코드가 적용되지 않는다.)
  
  따라서 이러한 문제점을 해결하기 위해 과거에는 selenium과 같은 브라우저 제어 프로그램을 사용하여 크롤러를 제작하였다.  하지만 웹 브라우저를 제어하기 위해서는 Web Driver를 설치하여 사전 셋팅 작업이 필요하다.
  
  여기서는 requests-html 이라는 모듈을 사용하여 javascript를 사용하여  동적으로 html 코드가 변경되는 페이지도 크롤링을 해볼 예정이다.(내부적으로 pyppeteer라는 모듈을 사용하여 javascript를 처리하며 이 모듈은 google에서 만들었으며 selenium보다 속도가 빠르고 최근 트랜드라고 한다.) 다만 python 버전이 3.6 버전만 가능하다는 단점이 있지만 크게 문제가 되지 않을 것이라 생각한다.
  
  :bulb: **공식 Github 사이트 :** `https://github.com/psf/requests-html`
  
  :bulb: **설치 명령어 :** `pip install requests-html`
  
  우분투의 경우 동작에 필요한 라이브러리가 설치되지 않아 실행시 오류가 발생하므로 먼저 관련  라이브러리를 설치하여 준다.
  
  :bulb: **라이브러리 설치 명령어 :** `apt-get install gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget`
  
  먼저 코드를 작성하기 앞서 javascript로 페이지가 동적으로 변하는 페이지를 대상으로 크롤링을 수행하는 예제를 작성해본다.
  
  ```python
  from requests_html import HTMLSession

  session = HTMLSession();
  r = session.get('https://pythonclock.org')

  #run without javascript rendering
  tmp = r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0]
  print("run without javascript rendering ",tmp)
  print("")

  #Run With Javascript Rendering
  r.html.render()
  tmp = r.html.search('Python 2.7 will retire in...{}Enable Guido Mode')[0]
  print("run with javascript rendering ",tmp)
  ```
  
  테스트 결과 화면은 다음과 같으며 결과의 윗부분은 javascript를 실행하지 않은 크롤링 결과이며 아래부분은 javascript를 실행한 결과이다. (그림을 더블클릭하면 큰 화면으로 볼 수 있다.)
  
  크롤링 대상 사이트인 https://pythonclock.org에 가서 직접 소스보기를 해도 아래의 결과와 같은 것을 볼 수 있을 것이다. 이처럼 javascript로 이루어진 페이지를 크롤링하는 경우 추가적인 작업이 필요하다.
  
  ### 예제 01. 보안뉴스 기사 크롤링
  
    보안 뉴스 취약점 권고 및 보안 업데이트 페이지의 경우 다음과 같은 레이아웃의 형태로 되어 있다. 총 3부분으로 나눌 수 있는데 상단의 메뉴 부분을 제외하면 왼쪽은 기사가 오른쪽은 광고 및 기사 랭킹 순위로 구성되어 있다. 우리는 왼쪽의 기사 제목과 내용 요약 부분을 크롤링 할 예정이다.
    
    코드 구현에 앞서 우리가 수집해야할 정보만 크롤링 해 올 수 있도록 크롬의 개발자 도구를 통해 html 코드를 먼저 분석해보도록 한다.
    
    F12 키를 누르게 되면 다음 그림과 같이 크롬의 개발자 도구가 뜨게된다. Elements 탭에서 뜨는 html 코드를 분석하여 우리가 원하는 정보가 위치한 태그를 찾을 수도 있지만 우리는 빠르게 찾기 위해 다른 방법을 사용하도록 한다.
    
    Elements 탭 왼쪽에 보면 빨간 네모칸으로 표시된 화살표 모양 버튼을 클릭한다. 그럼 버튼이 파란색으로 변하며 마우스를 페이지에 올렸을 때 영역이 반투명 파란 박스가 내용의 위에 표시되며 해당 영역의 태그 정보를 같이 표시한다. 이때 마우스를 클릭하게 되면 Elements 탭의 코드 위치가 방금 마우스로 클릭한 html 코드의 위치로 이동하게 된다.
    
    이렇게 우리는 보안뉴스의 기사 리스트는 news_list라는 클래스명을 가진 div 태그로 묶여 있다는 것을 확인하였다. div 태그 왼쪽의 삼각형 모양을 누르게 되면 확장되며 제목부분과 내용 부분이 나뉘어 진 것을 확인할 수 있으며 제목부분의 클래스명은 news_txt고 span 태그로 묶여 있는 것을 볼 수 있다. 
    
    앞에서 우리가 크롤링 해야하는 정보가 담긴 태그와 클래스명을 확인하였다. 보통 태그의 경우 중복이 많기 때문에 원하는 부분만 추출이 힘들다. 하지만 html에서 클래스명은 css를 사용하여 그 태그를 원하는 형태로 꾸며주기 위해 사용하기 때문에 고유하거나 같은 내용을 가지고 있는 그룹들만 사용하게 된다. 따라서 이 클래스명을 사용하여 크롤링을 하는 코드를 작성해보도록 하겠다.
    
    아래의 코드는 news_list라는 클래스명을 가진 태그 객체들 모두 모아 기사의 제목과 내용 요약을 출력해주는 코드이다.
    
    ```python
      from requests_html import HTMLSession

      session = HTMLSession();
      r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')

      #Get News Title & Content Summary
      for line in r.html.find('.news_list'):
        print(line.text)
        print("")
    ```
  
  
    코드를 간단하게 설명해보자면 다음과 같다.
   
     ```python
       session = HTMLSession();
     ```
     
     웹 페이지에 접속하기 위해 준비하는 과정으로 일을 시키기 위한 일꾼을 준비시키는 과정이다.
     
     ```python
       r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')
     ```
     
     어떤 URL 웹 페이지에 접속할지 지정해주고 접속한 결과를 r이라는 변수에 담아주는 부분이다.
     
     ```python
       for line in r.html.find('.news_list'):
         print(line.text)
         print("")
     ```
     
     r 이라는 변수에는 웹 페이지에 접속한 결과를 가지고 있는 객체가 저장된다. 따라서 html이라는 메소드(함수)를 붙여서 사용하여 r이라는 객체가 얻어온 html 코드를 얻어오며 여기서 한번 더 find라는 메소드(함수)를 사용하여 우리가 찾고 싶은 태그 / 문자열 / 클래스명 등 을 넘겨줘 원하는 태그 객체만 얻어올 수 있도록 한다.
     
     따라서 얻어온 태그 객체들은 python의 리스트 형식으로 구성되어지며 for 문을 사용하여 하나씩 꺼내 해당 태그 객체의 텍스트를 출력하는 구조로 되어있다.
     
     위의 코드를 실행한 결과 화면은 아래와 같다. (잘 안보이는 경우 그림 더블 클릭)
     
     두번째 코드는 뉴스 기사의 제목 부분만 가져오는 코드이다.
     
     ```python
       from requests_html import HTMLSession

       session = HTMLSession();
       r = session.get('https://www.boannews.com/media/s_list.asp?skind=5')

       #Get News Title
       for news_num, news_title in enumerate( r.html.find('.news_txt') ):
         print( "[{}] {}".format(news_num, news_title.text) )
         print("")
     ```
     
     위에서 설명한 코드와 다른 부분만 설명하도록 하겠다.
     
     ```python
       for news_num, news_title in enumerate( r.html.find('.news_txt') ):
          print( "[{}] {}".format(news_num, news_title.text) )
          print("")
     ```
     
     for문에서 달라진 부분은 r.html.find 앞부분에 enumerate 함수가 추가되었다는 점이다. enumerate 함수의 경우 해당 리스트 값과 반환된 값의 인덱스 번호를 같이 반환한다. print의 서식문자열을 사용하여 뉴스 기사 번호와 뉴스 기사 제목을 출력하는 부분이다.
     
  ### 예제 02. 네이버 뉴스 기사 크롤링
  
     특정 단어의 네이버 뉴스 기사의 경우 다음과 같은 레이아웃의 형태로 되어 있다.  마찬가지로 총 3부분으로 나눌 수 있는데 상단의 검색 메뉴 부분을 제외하면 왼쪽은 기사 목록이 오른쪽은 검색어 랭킹 순위로 구성되어 있다. 우리는 왼쪽의 기사 제목과 내용 요약 부분을 크롤링 할 예정이다.
     
     위의 예제 1에서 설명했던 방법과 같이 특정 단어의 네이버 뉴스 기사 검색 내용 중 우리가 원하는 부분의 태그를 찾아보았다. 다만 네이버는 클래스명이 아닌 태그에 ID 값을 사용하였지만 ID값도 클래스명과 비슷하게 같은 태그들을 그룹화 시켜주는 역할을 하므로 비슷한 역할을 하는 친구로 이해하면 된다. 하지만 뒤에 숫자가 붙어서 완전히 문자열이 일치해야만 얻어오는 모듈의 특성상 크롤링에 어려움이 있다.
     
     따라서 여기서는 예제1에서 사용했던 클래스명을 이용하여 크롤링을 했던것처럼 ID값을 가지고 크롤링을 할 수 있지만 문자열 뒤에 일일이 숫자를 붙여가며 찾아내야 해서 코드가 지저분해지기 때문에 다른 방법을 사용하도록 하겠다.
     
     아래 그림에서 빨간 네모칸으로 되어 있는 부분을 보면 현재 선택된 태그가 최상위 태그인 html 태그를 기준으로 어떤 태그 아래에 있는지 나열한 부분이다.  사람으로 치면 내 조상이 누구인가를 확인하는 작업과 같으며 우리는 이 정보를 사용하여 원하는 정보를 크롤링 하도록 할 것이다.
     
     아래의 코드는 네이버기사 검색 결과를 크롤링 해오는 코드이다.
     
     ```python
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
     ```
     
     코드를 간단하게 설명해보자면 다음과 같다.
     
     ```python
       import urllib.parse as url_parse

       s_urlenc=url_parse.quote("랜섬웨어")
     ```
     
     영어로 된 검색어면 바로 입력이 가능하겠지만 URL에서 한글은 사용이 불가능하다. 하지만 크롬이나 기타 몇몇 브라우저에서는 한글을 표시해주기도 한다. 이것은 내부적으로는 변환 과정을 거쳐 서버로 전송하고 주소표시줄에만 한글을 표시해 주는 것이다.  따라서 우리 코드에서 한글이 들어간 부분은 URL Encode 과정을 통해 사용 가능한 문자열로 변환해야하며 이때 사용하는 것이 urllib.parse 모듈의 quote라는 메소드(함수)이다. 
     
     ```python
       r = session.get('https://search.naver.com/search.naver?where=news&query='+s_urlenc)
     ```
     
     다른 대부분의 검색 엔진들도 대부분 위의 네이버 검색 URL처럼 query 부분에 넘겨진 인자를 검색할 단어로 사용한다. 따라서 우리는 위에서 단어를 인코딩한 결과를 query에 인자로 넘겨줄 것이며 where 부분은 여기서 고정이긴하지만 news의 의미는 모든 검색 결과를 출력하는 것이 아닌 뉴스로 한정하겠다는 것을 의미한다. where 부분을 image로 바꾸면 이미지 검색 결과를 그리고 post로 바꾸면 블로그 검색 결과를 가져오게 된다. (이 부분은 네이버에서 자체적으로 정의한 결과이기 때문에 검색 엔진마다 다를 수 있다)
     
     ```python
        tag_sel='body > #wrap > #container > #content > #main_pack > div > ul.type01 > li'
     ```
     
     위에서 크롬 브라우저의 개발자 도구를 통해 확인한 태그 경로를 입력한 코드이다. body 태그를 기준으로 그 아래 태그들을 선택하는 과정이며 우리가 원하는 기사의 모음은 type01이라는 클래스 명을 가진 ul 태그가 가지고 있으며 각각의 기사들은 li 태그로 묶여져 구성되기 때문에 body > #wrap > #container > #content > #main_pack > div > ul.type01 아래에 있는 모든 li 태그들을 가져오도록 할 것이다.
     
     ```python
       for news_num, news_title in enumerate( r.html.find(tag_sel) ):
          print( "[{}] {}".format(news_num, news_title.text) )
          print("")
     ```
     
     r.html.find(tag_sel) 을 사용하여 위에서 지정한 태그 경로의 값을 불러와 검색을 시도한다.
     
     결과는 아래 그림과 같다.
     
     
