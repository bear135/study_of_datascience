## Chp 15. 파이썬과 MySQL 응용 프로그래밍

- MySQL에서 sample DB 생성 
```
DROP DATABASE IF EXISTS HANBITDB ; 
CREATE DATABASE HANBITDB ; 
```

- 파이썬에서 SQL 테이블을 생성하고 데이터 입력 
```
#! pip install pymysql 
import pymysql

## DB와 연결 
conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = '1234',
                       db = 'hanbitDB', charset = 'utf8')

## 커서 생성 
cur = conn.cursor() 
## 테이블 생성 
cur.execute("create table if not exists usertbl ( \
                id char(4), username char(15), email char(20), birthyear int) \
            ")

## 테이블에 데이터 입력
cur.execute("insert into usertbl values('john','John Bann','john@naver.com',1990)")
cur.execute("insert into usertbl values('kim','Kim Kei','kkei@daum.com',1994)")
cur.execute("insert into usertbl values('lee','Lee Miju','miju@kakao.com',1998)")
cur.execute("insert into usertbl values('kna','J Karina','karina@google.com',2001)")
cur.execute("insert into usertbl values('yu','Yu Cristal','y_cristal@gmail.com',1995)")

## 데이터 저장하고 닫기
conn.commit()
conn.close()
```

- 데이터 조회, 출력하기 
```
## 데이터 조회 
con, cur = None, None
data1, data2, data3, data4 = "", "", "", ""
row = None

conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = '1234',
                       db = 'hanbitDB', charset = 'utf8')

cur = conn.cursor() 
cur.execute("select * from usertbl")

print('ID     Name     Email     Birth_Year')
print('----------------------------------------')

while (True) : 
    row = cur.fetchone()
    if row == None : 
        break 
    data1 = row[0]
    data2 = row[1]
    data3 = row[2]
    data4 = row[3]
    
    print(data1,data2,data3,data4)
    
conn.close()
```
