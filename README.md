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

---------------------------------------
# Docker 상세 설명
> 각 도커 서비스 별로 추가적인 설명

crwling + elasticsearch + logstash + kibana + mysql


## 1. crawling
### 1.1 기본 정보
> 파이썬 도커 이미지를 기반으로 만들어져 있으며, 
* Dockerfile 파일: `docker/crawling/Dockerfile`
* 설정 폴더: `docker/crawling/`
* python 3.6.8

### 1.2 entrypoint.sh
- entrypoint.sh: 도커 실행시 docker-compose.yml 의 command 에서 시작하게 설정 및 volume에 추가 시켜 놓음.
- create_logstash_db.py init_mapping.py  파일을 자동으로 시작하게 설정되어 있음.
- dockerize -wait tcp://db:3306 -wait http://elasticsearch:9200 -timeout 50s.  <<---- dockerfile 안에 셋팅 및 다운로드 시켜놓았기 때문에 동작함.
- init_mapping.py와 create_logstash_db는 기본적으로 실행하는데 오랜 시간이 걸리는데, 이 때문에 50초동안 실행 대기하게 해놓음.
### 1.3 DOCKERIZE
### 1.4 cron_config
### 1.5 pip_requirements.txt
- 도커 이미지 만들때 pip install 을 해야할 패지키 목록들을 가지고 있음.

# crawling 폴더
- 도커이미지 파일(crawling)을 생성하는데 필요한 파일들이 들어있음
- 파일이름 수정시 전체 시스템이 동작하지 않을 수 있음. (docker-compose 참고)

# cron_config
- cron_config: 마지막 줄에 엔터를 꼭 쳐야함!(안그러면 동작안함. EOF 때문인듯) 
- cron_config: dos2unix 이거 안붙이면 로그파일 생성시 파일뒤에 ?라는 기호가 추가됨. 이것도 파일 저장과정에서 원치않은 데이터가 들어가는듯.(연구 필요) 

# entrypoint.sh
- entrypoint.sh: 도커 실행시 docker-compose.yml 의 command 에서 시작하게 설정 및 volume에 추가 시켜 놓음.
- create_logstash_db.py init_mapping.py  파일을 자동으로 시작하게 설정되어 있음.
- dockerize -wait tcp://db:3306 -wait http://elasticsearch:9200 -timeout 50s.  <<---- dockerfile 안에 셋팅 및 다운로드 시켜놓았기 때문에 동작함.
- init_mapping.py와 create_logstash_db는 기본적으로 실행하는데 오랜 시간이 걸리는데, 이 때문에 50초동안 실행 대기하게 해놓음.

# pip_requirements.txt
- 도커 이미지 만들때 pip install 을 해야할 패지키 목록들을 가지고 있음.

## 2. elasticsearch
### 1.1 기본정보
- 






# nori analyzer
- 한국에 분석 플러그인 노리(nori)
- userdict_ko.txt에 원하는 단어를 추가 시킬 수 있다. (docker-compose.yml 파일 참고)

# Kibana Dashboard 셋팅법
> 키바나에서 시각화 방법은 아래 링크 참고해 주시길 바랍니다.
- 블로그 참고: https://epicarts.tistory.com/75

## 참고문서
* [ubuntu 도커 설치](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [엘라스틱서치 vm.max_map_count 설정](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)
