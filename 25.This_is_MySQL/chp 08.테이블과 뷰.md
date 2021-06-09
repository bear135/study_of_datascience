## Chp 08. 테이블과 뷰

**1. DB, Table 생성 후 데이터 입력** 
```
create database tabledb ; 

use tabledb ; 
DROP TABLE IF EXISTS buytbl, usertbl;

CREATE TABLE usertbl 
( userID  CHAR(8) NOT NULL PRIMARY KEY, 
  name    VARCHAR(10) NOT NULL, 
  birthYear   INT NOT NULL,  
  addr	  CHAR(2) NOT NULL,
  mobile1	CHAR(3) NULL, 
  mobile2   CHAR(8) NULL, 
  height    SMALLINT NULL, 
  mDate    DATE NULL 
);

CREATE TABLE buytbl 
(  num INT AUTO_INCREMENT NOT NULL PRIMARY KEY, 
   userid  CHAR(8) NOT NULL ,
   prodName CHAR(6) NOT NULL,
   groupName CHAR(4) NULL , 
   price     INT  NOT NULL,
   amount    SMALLINT  NOT NULL 
   , FOREIGN KEY(userid) REFERENCES usertbl(userID)
);

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
---
INSERT INTO buytbl VALUES(NULL, 'KBS', '운동화', NULL, 30, 2);
INSERT INTO buytbl VALUES(NULL, 'KBS', '노트북', '전자', 1000, 1);
INSERT INTO buytbl VALUES(NULL, 'JYP', '모니터', '전자', 200, 1);
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

**2. constraint (제약조건)** 
1) primary key : 중복불가, null값 불가 
2) foreign key : 두 테이블의 관계선언, 다른 테이블에 의존하게 된다. 
3) unique : 중복불가, null값은 가능 (ex. 회원가입시 unique한 email 주소 요구)
4) check : 지정된 조건을 만족하는 값만 입력가능하도록 함 
```
/*ex. 휴대폰 국번에 입력 가능한 값 제한 */
ALTER TABLE TABLEDB.USERTBL 
	ADD CONSTRAINT CK_MOBILE1
    CHECK (MOBILE1 IN ('010', '011', '016', '017', '019')) ; 
```
5) default : 값을 입력하지 않았을때 기본값 할당 
6) Null, Not Null : Null 값 허용여부 설정 

**3. 테이블 압축**
- 테이블 압축시 데이터 입력에는 좀더 시간이 걸리나, 
- 테이블의 avg_length, data_length등이 짧아진다. (공간절약) 
```
CREATE DATABASE IF NOT EXISTS COMPRESSDB ; 
USE COMPRESSDB ; 
-- normal vs compress 
CREATE TABLE NORMALtbl(EMP_NO INT, FIRST_NAME VARCHAR(14)) ; 
CREATE TABLE COMPRESStbl(EMP_NO INT, FIRST_NAME VARCHAR(14))  
	ROW_FORMAT = COMPRESSED ; 

INSERT INTO NORMALTBL 
	SELECT EMP_NO, FIRST_NAME 
    FROM EMPLOYEES.EMPLOYEES ;   /* 2.281 sec*/ 

INSERT INTO COMPRESSTBL
	SELECT EMP_NO, FIRST_NAME 
    FROM EMPLOYEES.EMPLOYEES ;   /* 5.110 sec*/ 
    
SHOW TABLE STATUS FROM COMPRESSDB ; 
```

**4. temporary table** 
- 임시테이블은 session 내에서만 존재, 세션 종료시 자동 삭제됨 
```
CREATE temporary TABLE NORMALtbl(EMP_NO INT, FIRST_NAME VARCHAR(14)) ; 
```
**5. Drop table**
- DROP TABLE *table_name1, table_name2, table_name3, ...*  ; 
- Foreign key 제약조건의 기준테이블은 삭제 불가, 예를들어 buy table이 존재하는 상태에서 user table을 삭제할 수 없다. 

**6. Alter table**
- 홈페이지 주소 컬럼 추가 (입력값 없을시 구글, null값 허용) 
```
ALTER TABLE TABLEDB.USERTBL 
	ADD HOMEPAGE VARCHAR(30) 
		DEFAULT 'HTTP://WWW.GOOGLE.COM' NULL ; 
```
- name --> user_name으로 변경 (20 digits 문자열, null값 허용) 
```
ALTER TABLE TABLEDB.USERTBL 
	CHANGE COLUMN  NAME USER_NAME VARCHAR(20) NULL ; 
```
**7. View ** 
- view의 생성과 삭제 : create view, drop view 
```
CREATE VIEW V_USERTBL 
AS  SELECT USERID, USER_NAME, ADDR 
 	FROM TABLEDB.USERTBL ; 
```

