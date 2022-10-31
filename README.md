
# 실행방법
 * python main.py
 * main.py의 포트로 실행
 * 확인 : localhost:port

폴더 구조
* common : 공통모듈
* database : database 연결 및 database model
* repository : database에 접근
* route : 엔드포인트 router
* scemas : reqeust, response model
* services : 서비스 service
* utils : util

 app
   │
   ├── app/                                 - 어플리케이션 폴더
   │   ├── common                           - 공통폴더
   │   │   |── enum                        - enum 타입 정의
   │   │   |── exeception                  - exception 정의
   │   │   |── middleware                  - moddle ware
   │   │   │
   │   ├── database/                  
   │   │   ├── model                        - database model
   │   │   ├── database.py                  - database connect          
   │   │   │
   │   ├── repository/                                
   │   │   │   ├── __init__.py              
   │   │   │   ├── auth_repository.py       - database 접근하기위한 repository 
   │   │   │
   │   ├── scemas/                                 
   │   │   ├── __init__.py              
   │   │   ├── auth.py                      - request, response model
   │   │   |    
   │   ├── services/         
   │   │   ├── __init__.py
   │   │   ├── auth_handler                 - handler
   │   │   │
   │   ├── utils/
   │   │   ├── auth.py                      - 권한관련 util
   │   │   ├── geometry.py                  - 좌표관련 util
   │   │   ├── http_request.py              - request 관련 util
   │   │   ├── session_context.py           - db session 관련 util
   │   │   ├── timestamp.py                 - 시간 관련 util
   
   │   ├── test_api.py                      - fast_api 정의
   │ 
   ├── test                                 - 테스트 폴더
   ├── README.md                            - README
   └── define.py                            - ROOT_DIR , SERVER_NAME 등 정의
   └── main.py                              - server name, port 설정, 실행 시 python main.py
   └── requirements.txt                     - 필요 모듈 정리
