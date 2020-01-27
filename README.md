# team-crawlcrawl
> 보안뉴스 실시간 크롤링 및 데이터 시각화 (2019 캡스톤 디자인 프로젝트)

몇몇의 보안뉴스 사이트에서 자동으로 페이지를 크롤링하여, 엘라스틱서치에 저장 후 키바나로 시각화하였습니다.

![kibana](https://user-images.githubusercontent.com/17478634/73137801-6fecf780-409f-11ea-9dd2-98edc122db62.PNG)


## 개발환경
> Docker 를 사용하여 환경 구성

* logstash == 7.3.2
* elasticsearch == 7.3.2
* kibana == 7.3.2
* python == 3.6.8
* mysql == 8.0.18

## 프로젝트 구성도
<img src="https://user-images.githubusercontent.com/17478634/73138072-ee4a9900-40a1-11ea-8d69-46f2fddff5f8.PNG" height="300px" ></img><br/>


### 순서
	1. 뉴스 데이터를 일정시간 마다 자동으로 데이터 크롤링
	2. 수집한 데이터를 MySQL에 저장.
	3. MySQL에 저장된 뉴스 데이터에서 키워드 3개 추출 후 다시 MySQL에 저장. 
	4. Logstash를 사용하여 MySQL 데이터를 ElasticSearch에 저장
	5. Kibana를 통해서 ElasticSearh에 저장된 데이터를 시각화 
	6. 웹페이지를 통해 사용자에게 검색 서비스 제공(미구현)

---------------------------------------

# 실행 방법
* OS: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type(AWS EC2)
* 권장 사양: RAM 8GB

## 1. Docker 설치
### 1.1 설치 사전 준비
```sh
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
```
### 1.2. Docker 설치하기
```sh
sudo apt-get install docker-ce
```

### 1.3. Docker-compose 설치하기
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 2. Docker 실행

### 2.1 git clone
`git clone https://github.com/epicarts/team-crawlcrawl.git` 깃허브에서 폴더 복제

`cd team-crawlcrawl/` 다운 받은 폴더로 이동

### 2.2 권한 및 메모리 셋팅
`sudo sysctl -w vm.max_map_count=262144` 엘라스틱서치 사용을 위한 메모리 셋팅

`sudo chown 1000:1000 -R ./docker/logstash/last_run_metadata/` 로그스태쉬 파일 기록을 위한 권한 셋팅

### 2.3 Docker-compose 빌드 및 실행
`sudo docker-compose up --build` 도커 컴포즈 실행 및 빌드

## 3. kibana 접속
### 3.1 kibana
모든 도커 서비스가 정상적으로 가동되면 kibana 통해 웹페이지를 통해 접속 할 수 있다.

Docker-compose 에서 기존 `5601 port` 에서 `80 port`로 변경을 하였기 떄문에 로컬 환경에서 웹브라우저를 사용해 `127.0.0.1` 로 접속할 수 있다.(Chrome 권장) 


---------------------------------------
# Docker 상세 설명
> 각 도커 서비스 별로 추가적인 설명

crwling + elasticsearch + logstash + kibana + mysql


## 1. crawling
### 1.1 기본 정보
> python을 기반으로 데이터 자동 수집과 디비 생성, 엘라스틱서치 맵핑 역할 수행
* Dockerfile 파일: `docker/crawling/Dockerfile`
* 설정 폴더: `docker/crawling/`
* `python 3.6.8`
### 1.2 entrypoint.sh
> cron 기능을 사용하기 위한 권한 설정 및 다른 컨테이너와 종속성을 위해 만든 sh 파일
* create_mysql_table.py init_mapping.py  파일을 자동으로 시작하게 설정되어 있음.
* `dockerize -wait tcp://db:3306 -wait http://elasticsearch:9200 -timeout 50s.` 다른 컨테이너내의 서비스가 실행되기 기다림.
* init_mapping.py와 create_mysql_table는 기본적으로 실행하는데 오랜 시간이 걸리는데, 이 때문에 50초동안 실행 대기하게 해놓음.
### 1.3 DOCKERIZE v0.6.1
> 서비스 종속성을 위한 유틸리티
* `Dockerfile` 에서 다운로드 후 `entrypoint.sh`에서 사용
* https://github.com/jwilder/dockerize 
### 1.4 cron_config
* 마지막 줄에 엔터를 꼭 쳐야함!(EOF로 인한 동작오류 추정) 
* `dos2unix` 안붙이면 로그파일 생성시 파일뒤에 `?`라는 기호가 추가됨.
* `crawling_code/crontab_python/`에 위치한 코드들을 반복실행
* `crawling_code/nlp_model/keyword_extraction.py` 
### 1.5 pip_requirements.txt
* Docker 이미지 생성시 사용되는 pip install 패키지 목록


## 2. Elasticsearch
### 2.1 기본정보
> 데이터 검색 엔진
* Dockerfile 파일: `docker/elasticsearch/Dockerfile`
* 설정 폴더: `docker/elasticsearch/`
* `elasticsearch 7.3.2`
### 2.2 Dockerfile
* `RUN bin/elasticsearch-plugin install analysis-nori` [노리 플러그인](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori.html) 사용을 위해 설치
### 2.3 nori analyzer
* 한국어 분석 플러그인 노리(nori)
* `docker/elasticsearch/userdict_ko.txt`에 원하는 사용자 정의 단어 추가 가능.

## 3. Logstash 
### 3.1 기본정보
> MySQL과 Elasticsearch 사이에서 데이터 파이프 라인 역할 수행
* 설정 폴더: `docker/logstash/`
* `Logstash 7.3.2`
### 3.2 last_run_metadata 폴더
* `jdbc-int-sql_last_value.yml` 파일 자동 생성(gitignore 등록되어 있음) 
* `jdbc-int-sql_last_value.yml` 은 MYSQL에서 엘라스틱서치로 넣을 때 현재 넣은 위치를 트래킹해주는 역할을 함. 
* `--- 1580101024` UNIX_TIMESTAMP 값으로 구성
### 3.3 pipline 폴더
* 로그스태시에서 자동으로 실행될 파이프라인 설정 파일들을 모아놓은 폴더
* 폴더째로 동작하기 떄문에 필요없는 데이터를 넣어놓으면 안됨
### 3.4 pipline/pipline.conf
* input: jdbc 플러그인을 활용하여 MySQL에서 마지막으로 읽은 문서 추적 및 수집
* filter: 필요없는 데이터 삭제 및 가공
* output: Elasticsearch 플러그인을 활용하여 Elasticsearch에 데이터 전달
### 3.5 driver 폴더
* jdbc 모듈을 사용하기 위한 `mysql-connector-java-5.1.48-bin.jar` 파일 위치
### 3.6 config 폴더
* 로그스태시의 기본적인 설정들을 할 수 있는 폴더

## 4. MySQL
### 4.1 기본정보
> 크롤러를 사용하여 수집한 데이터를 저장해 놓은 관계형 데이터베이스
* `Mysql 8.0.18`


## 5. kibana
### 5.1 기본정보
> Elasticsearch에 저장된 데이터를 시각화
* `kibana 7.3.2`
### 5.2 Kibana Dashboard 셋팅법
> 키바나에서 시각화 방법은 아래 링크 참고해 주시길 바랍니다.
- 블로그 참고: https://epicarts.tistory.com/75

## 참고문서
* [ubuntu 도커 설치](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [엘라스틱서치 vm.max_map_count 설정](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)
* [노리 플러그인](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-nori.html)
* [Logstash JDBC 데이터베이스 동기화](https://www.elastic.co/kr/blog/how-to-keep-elasticsearch-synchronized-with-a-relational-database-using-logstash)