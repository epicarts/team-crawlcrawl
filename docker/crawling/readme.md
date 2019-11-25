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