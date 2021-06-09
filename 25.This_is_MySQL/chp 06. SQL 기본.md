## Chp 06. SQL 기본 

1. Tip 
```
## DB를 지정하고 그 안의 tables 현황 조회 시 
use employees ; 
show table status ;  

## 특정 테이블의 컬럼정보를 확인할 때 
describe employees.employees ; 
describe shopdb.membertbl ; 
```

2. 실습용 DB 생성 
- sql이라는 이름의 DB 생성 (기존에 있다면 먼저 삭제) 
```
drop database if exists sqldb ; 
create database sqldb ; 
```
- 2개의 테이블 생성 
```
USE sqlDB;

CREATE TABLE userTbl -- 회원 테이블
( userID	CHAR(8) NOT NULL PRIMARY KEY,  -- 사용자아이디
  username	VARCHAR(10) NOT NULL, -- 이름
  birthYear INT NOT NULL,  -- 출생년도
  addr		CHAR(2) NOT NULL, -- 지역(경기,서울,경남 식으로 2글자만입력)
  mobile1 	CHAR(3), -- 휴대폰의 국번(011, 016, 017, 018, 019, 010 등)
  mobile2 	CHAR(8), -- 휴대폰의 나머지 전화번호(하이픈제외)
  height  	SMALLINT,  -- 키
  mDate   	DATE  -- 회원 가입일
);

CREATE TABLE buytbl -- 회원 구매 테이블(Buy Table의 약자)
(  num   INT AUTO_INCREMENT NOT NULL PRIMARY KEY, -- 순번(PK)
   userID   CHAR(8) NOT NULL, -- 아이디(FK)
   prodName  CHAR(6) NOT NULL, --  물품명
   groupName  CHAR(4)  , -- 분류
   price      INT  NOT NULL, -- 단가
   amount     SMALLINT  NOT NULL, -- 수량
   FOREIGN KEY (userID) REFERENCES usertbl(userID)
);
```
- 데이터 입력 
```
INSERT INTO usertbl VALUES('LSG', '이승기', 1987, '서울', '011', '1111111', 182, '2008-8-8');
INSERT INTO usertbl VALUES('KBS', '김범수', 1979, '경남', '011', '2222222', 173, '2012-4-4');
INSERT INTO usertbl VALUES('KKH', '김경호', 1971, '전남', '019', '3333333', 177, '2007-7-7');
INSERT INTO usertbl VALUES('JYP', '조용필', 1950, '경기', '011', '4444444', 166, '2009-4-4');
INSERT INTO usertbl VALUES('SSK', '성시경', 1979, '서울', NULL  , NULL      , 186, '2013-12-12');
INSERT INTO usertbl VALUES('LJB', '임재범', 1963, '서울', '016', '6666666', 182, '2009-9-9');
INSERT INTO usertbl VALUES('YJS', '윤종신', 1969, '경남', NULL  , NULL      , 170, '2005-5-5');
INSERT INTO usertbl VALUES('EJW', '은지원', 1972, '경북', '011', '8888888', 174, '2014-3-3');
INSERT INTO usertbl VALUES('JKW', '조관우', 1965, '경기', '018', '9999999', 172, '2010-10-10');
INSERT INTO usertbl VALUES('BBK', '바비킴', 1973, '서울', '010', '0000000', 176, '2013-5-5');

INSERT INTO buytbl VALUES(NULL, 'KBS', '운동화', NULL   , 30,   2);
INSERT INTO buytbl VALUES(NULL, 'KBS', '노트북', '전자', 1000, 1);
INSERT INTO buytbl VALUES(NULL, 'JYP', '모니터', '전자', 200,  1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '모니터', '전자', 200,  5);
INSERT INTO buytbl VALUES(NULL, 'KBS', '청바지', '의류', 50,   3);
INSERT INTO buytbl VALUES(NULL, 'BBK', '메모리', '전자', 80,  10);
INSERT INTO buytbl VALUES(NULL, 'SSK', '책'    , '서적', 15,   5);
INSERT INTO buytbl VALUES(NULL, 'EJW', '책'    , '서적', 15,   2);
INSERT INTO buytbl VALUES(NULL, 'EJW', '청바지', '의류', 50,   1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '운동화', NULL   , 30,   2);
INSERT INTO buytbl VALUES(NULL, 'EJW', '책'    , '서적', 15,   1);
INSERT INTO buytbl VALUES(NULL, 'BBK', '운동화', NULL   , 30,   2);
```

3. Tip : wild card 
- %는 뭐든 허용, _는 한글자만 허용 
- ex) '%용준'  ⇒ 김용준, 희고푸른용준 등...
- ex) '_용준'  ⇒ 김용준, 조용준, 박용준 등... 

4. Sub query와 ANY/ALL 
- where 조건절에 sub query 사용시, sub query의 return 값이 하나여야 한다. 
- 만약 return값이 둘 이상일 경우, 하나의 값만 만족해도 좋다면 ANY를, 모든 조건을 만족해야 한다면 ALL 함수를 사용한다.  
```
SELECT     username, height
FROM	   sqldb.usertbl
WHERE
    height >= ANY (SELECT height FROM sqldb.usertbl WHERE addr = '경남') 
; 
```
```
SELECT     username, height
FROM	   sqldb.usertbl
WHERE
    height >= ALL (SELECT height FROM sqldb.usertbl WHERE addr = '경남') 
; 
```
5. 복합정렬 
```
SELECT     username, height
FROM       sqldb.usertbl
ORDER BY height desc, username asc ; 
```

6. create table을 사용하여 기존 테이블의 일부만 복사하기 
- 단 이때 key 정보는 복사되지 않는다. 
```
CREATE TABLE buytbl13 (
	SELECT  userid, prodname 
	FROM    sqldb.buytbl
); 
```

7. 집계함수 
- sum, min, max, avg, count, count(distinct), stdev, var_samp()
```
SELECT     prodname, AVG(amount) AS 'avg_qty'
FROM       sqldb.buytbl
GROUP BY   prodname 
; 
```
```
SELECT     userid, SUM(price*amount) as total_sales
FROM       sqldb.buytbl
GROUP BY   userid
; 
```
```
SELECT     username, height
FROM       sqldb.usertbl
WHERE
    height = (SELECT MAX(height) FROM usertbl)
	OR height = (SELECT MIN(height) FROM usertbl)
; 
```

8. Having 
- where 조건절에서는 집계함수를 사용할 수 없다. 
```
SELECT     userid, SUM(price * amount) AS total_sales
FROM       sqldb.buytbl
GROUP BY   userid
HAVING     total_sales > 1000
ORDER BY   total_sales desc 
; 
```

9. ROLLUP for sub total
- 아래 구문에서 groupname을 기준으로 sub total이, num을 대상으로 total이 구해진다. 
```
SELECT     num, groupname, sum(price*amount) as tot_sales 
FROM       sqldb.buytbl
GROUP BY   groupname, num
WITH ROLLUP 
; 
```
10. SQL의 분류
- DML(Data Manipulation Language) 
   - 테이블의 row를 대상으로 함, 따라서 반드시 테이블 사전 정의 필요 
    - select, insert, delete, update 등 
 - DDL(Data Definition Language) 
    - object를 생성/삭제/변경 
    - create, alter, drop 등 
 - DCL(Data Constrol Language) 
    - 사용자 권한 관련 : grant, revoke, deny 등  

*cf. DML은 transaction이 발생하므로 속도가 느린 대신 roll back이 가능, 
     DDL은 transaction 미발생, roll back 불가* 

11. Insert 
- 테이블에 데이터 삽입 
```
CREATE TABLE testtbl (id INT, username CHAR(10), age INT) ;
INSERT INTO testtbl(id, username, age) VALUES (2, 'Yunna', 27); 
```

12. Auto_Increment 
- 자동으로 1부터 증가하는 값을 입력해줌 
- 반드시 해당 컬럼을 primary key로 지정해야 함 
- insert 문으로 데이터 입력시, 해당 컬럼은 null로 처리 
```
CREATE TABLE testtbl2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username CHAR(10),
    age INT
);

INSERT INTO testtbl2 values (NULL, 'Key', 23), 
							(NULL, 'Jisu', 21), 
							(NULL, 'Soul', 20), 
                            (NULL, 'Miju', 24) ; 
```

13. 빈 테이블을 만들고, 기존 DB를 가져와 넣기 
```
CREATE TABLE sqldb.testtbl4(
	SELECT emp_no, first_name, last_name 
    FROM employees.employees
    LIMIT 10000 
    ) ; 
```

14. Update 
```
## 특정조건을 가진 row에 대해 값을 바꾼다. 
UPDATE sqldb.testtbl4 
	SET     last_name = 'None'
	WHERE    first_name = 'Kyoichi'
;
## 테이블 전체를 업뎃한다. 
UPDATE sqldb.buytbl 
	SET     price = (price * 1.5); 
```
15. Delete 
```
## 해당조건의 상위 10개만 삭제
delete from sqldb.tasttbl4 
	   where first_name = 'Aamer' limit 10 ; 
```

16. With 
- with문을 사용하여 쿼리를 단순화 할 수 있다. 
```
## 가상의 temp_t를 만들고, 이것을 다시 정렬하는 구문 
WITH temp_t(userid, total) AS 
	(SELECT     userid, SUM(price * amount)
	 FROM       sqldb.buytbl
	 GROUP BY   userid)
SELECT * FROM temp_t ORDER BY total DESC ; 
```
```
## 각 지역별 max height를 구한 후, 이들의 평균 구하기 
with temp_2 (addr, max_height) as (
	 select addr, max(height) 
     from sqldb.usertbl
     group by addr) 
select avg(max_height) from temp_2 ; 
```

