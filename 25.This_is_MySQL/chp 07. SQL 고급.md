## Chp 07. SQL 고급 

**1. Data type** 
- INT : 정수 
- Float, Double : 실수 
- char(), varchar() : 문자 
```
char()은 자릿수가 고정되어 있음. 
반면 varchar()은 자릿수가 가변적이다. 

ex) char(10)이면 3 digit만 입력해도 해당변수는 10 digits을 차지한다. 
ex) varchar(10)일때 3 digits만 입력하면 해당 변수의 digit은 3이다. 
```

- LONGTEXT : 4GB까지의 txt를 저장가능 
- LONGBLOB : 4GB까지의 object를 저장가능 (동영상 등) 

**2. 변수선언 : set @** 
```
set @myvar1 = 5 ; 
set @myvar2 = 4 ; 
set @myvar3 = 3 ; 

select @myvar1, @myvar2, @myvar3 ; 
# 5  4  3
```
```
set @myvar4 = 'Name ==> ' ; 

select @myvar4, username 
from sqldb.usertbl 
where height > 180 ;  

# Name ==> 임재범  Name ==> 이승기  Name ==> 성시경
```

**3. cast, convert** 
- as signed integer : 정수변환 
```
select avg(amount) as Average_Buying_Qty
from sqldb.buytbl ; 
## 2.9167

select cast(avg(amount) as signed integer) as Average_Buying_Qty
from sqldb.buytbl ; 
## 3 
```
- 날짜 포맷으로 변환 
```
SELECT CAST('2020$12$12' AS DATE); 
SELECT CAST('2020/12/12' AS DATE); 
SELECT CAST('2020|12|12' AS DATE); 
## 2020-12-12 
```

**4. IFNULL** 
```
select ifnull(null, 100) ; ## --> 100 
select ifnull(0, 100) ; ## --> 0
```
**5. CASE ~ WHEN ~ ELSE ~ AS** 
```
SELECT 
    CASE 10
        WHEN 1 THEN 'one'
        WHEN 5 THEN 'five'
        WHEN 10 THEN 'ten'
        ELSE 'don\'t know'	
    END AS 'output' ;   ## --> ten 
```
```    
SELECT 
    CASE 100
        WHEN 1 THEN 'one'
        WHEN 5 THEN 'five'
        WHEN 10 THEN 'ten'
        ELSE 'don\'t know'	
    END AS 'output' ;   ## --> don't know
```
**6. CONCAT, CONCAT_WS**
```
SELECT CONCAT('2021', '-', '01', '-', '01'); ## 2021-01-01
SELECT CONCAT_WS('-', '2021', '01', '01'); ## 2021-01-01
```
**7. FIELD**
- field(찾을 문자열, 문자열~) 
```
select field('둘', '하나','둘','셋','넷','다섯') ; ## 2
```
**8. FORMAT**
- 소수점 지정 & 100단위 구분 
```
select format(12345.6789, 3);   ## 12,345.679
```
**9. INSERT**
- 문자열의 a번째부터 b칸만큼을 지정된 문자열로 대체 
```
SELECT INSERT('abcdrfghi', 3, 4, '@@'); ## ab@@ghi
SELECT INSERT('abcdrfghi', 3, 4, '@@@@');  ## ab@@@@ghi
```
**10. LEFT, LIGHT**
```
SELECT LEFT('abcdrfghi', 3);   ## abc
SELECT RIGHT('abcdrfghi', 3);  ## ghi
```
**11. UPPER, LOWER**
```
SELECT UPPER('abcdrfghi');  ## ABCDRFGHI
SELECT LOWER('ABCDRFGHI');  ## abcdrfghi
```
**12. LPAD, RPAD**
- 빈칸을 지정된 문자열로 채운다 
```
## 전체 digits를 10으로 만든 후, 남은 공간을 -로 채운다. 
SELECT LPAD('This is', 10, '-'); ## ---This is
SELECT RPAD('This is', 10, '-'); ## This is---
```
**13. TRIM, LTRIM, RTRIM**
```
SELECT TRIM('     What the fuck!     ');  ## What the fuck!
SELECT LTRIM('     What the fuck!');  ## What the fuck!
SELECT RTRIM('What the fuck!     ');  ## What the fuck!
```
**14. REPEAT, REPLACE**
- repeat : 문자열을 지정된 횟수만큼 반복 
- replace : 문자열 중 a를 b로 바꾼다. 
```
select repeat('This', 3) ; ## ThisThisThis
select replace('이것이 MySQL 이다', '이것이', 'This is') ; ## This is MySQL 이다
```
**15. REVERSE, SPACE, SUBSTRING**
- reverse : 문자열을 거꾸로 
- space(k) : k개의 공백
- substring : 문자열의 a번째부터 b개를 반환 
```
select reverse('This is MySQL.') ; ## .LQSyM si sihT
select concat('This', space(10), 'MySQL.') ; ## This          MySQL.
select substring('This is MySQL.', 6,2) ; ## is
```
** 16. math function ** 
```
SELECT ABS (-200) ; ## 절대값 : 200 
SELECT CEILING(4.7) ; ## 올림 : 5
SELECT FLOOR(4.7) ; ## 내림 : 4
SELECT ROUND(4.7) ; ## 반올림 : 5
SELECT MOD(157, 10) ; ## 10으로 나눈 나머지 
SELECT POW(2,3) ; ## 2의 3승 : 8 
SELECT SQRT(9) ; ## 제곱근 : 3
SELECT RAND() ; ## 0~1사이의 난수
SELECT TRUNCATE(1234,5678) ; ## 소수점 절사 : 1234
```
**17. DATE, TIME**
```
SELECT CURRENT_DATE() ; ## 2021-05-23
SELECT CURRENT_TIME() ; ## 23:14:30
SELECT NOW() ; ## 2021-05-23 23:14:48 

SELECT YEAR('2021-05-23 23:14:48') ; ## 2021
SELECT MONTH('2021-05-23 23:14:48') ; ## 5
SELECT DAY('2021-05-23 23:14:48') ; ## 23
SELECT HOUR('2021-05-23 23:14:48') ; ## 23
SELECT MINUTE('2021-05-23 23:14:48') ; ## 14
SELECT SECOND('2021-05-23 23:14:48') ; ## 48

SELECT DATE('2021-05-23 23:14:48') ; ## 날짜만 추출 : 2021-05-23
SELECT TIME('2021-05-23 23:14:48') ; ## 날짜만 추출 : 23:14:48
```

**18. FOUND_ROW**
- 이전 select문에서 조회된 row의 갯수 
```
SELECT * FROM SQLDB.USERTBL LIMIT 5 ; 
SELECT FOUND_ROWS() ; ## 5 
```
**19. Pivot table**
```
SELECT * FROM SQLDB.buytbl ; 

### pivoting 
select prodname, 
	sum(if(groupname = '전자', amount, 0)) as '전자', 
    sum(if(groupname = '의류', amount, 0)) as '의류', 
    sum(if(groupname = '서적', amount, 0)) as '서적', 
    sum(if(groupname = null, amount, 0)) as 'Null', 
    sum(amount) as 'Total' 
from sqldb.buytbl 
group by prodname ; 
```
**20. JOIN** 
```
select * 
from sqldb.usertbl 
where userid = 'JYP' ; ## --> 회원의 프로파일 조회 

select * 
from sqldb.buytbl 
where userid = 'JYP' ; ## --> 회원의 구매정보 조회 

## 구매한 고객에게 배송을 위해 마스터(회원정보)로부터 주소를 조회해야 한다. 
## userID는 두 테이블에 모두 있으므로 --> buytbl.userID
select buytbl.userID, 
	   username, 
	   prodname, 
	   addr, 
	   concat(mobile1, mobile2) as '연락처'
from sqldb.buytbl join sqldb.usertbl 
	 on buytbl.userID = usertbl.userID 
where buytbl.userID = 'JYP' ; 
```
- 각 테이블에 별칭을 사용하여 코드를 간단하게 표현 하자 
```
select B.userID, 
	   U.username, 
	   B.prodname, 
	   U.addr, 
	   concat(U.mobile1, U.mobile2) as '연락처'
from sqldb.buytbl B join sqldb.usertbl U
	 on B.userID = U.userID 
where B.userID = 'JYP' ; 
```
**21. 3 tables join practice** 
```
## making the 3 tables 
USE sqldb;
CREATE TABLE stdtbl 
( stdName    VARCHAR(10) NOT NULL PRIMARY KEY,
  addr	  CHAR(4) NOT NULL
);
INSERT INTO stdtbl VALUES ('김범수','경남'), ('성시경','서울'), ('조용필','경기'), ('은지원','경북'),('바비킴','서울');

CREATE TABLE clubtbl 
( clubName    VARCHAR(10) NOT NULL PRIMARY KEY,
  roomNo    CHAR(4) NOT NULL
);
INSERT INTO clubtbl VALUES ('수영','101호'), ('바둑','102호'), ('축구','103호'), ('봉사','104호');

CREATE TABLE stdclubtbl
(  num int AUTO_INCREMENT NOT NULL PRIMARY KEY, 
   stdName    VARCHAR(10) NOT NULL,
   clubName    VARCHAR(10) NOT NULL,
FOREIGN KEY(stdName) REFERENCES stdtbl(stdName),
FOREIGN KEY(clubName) REFERENCES clubtbl(clubName)
);
INSERT INTO stdclubtbl VALUES (NULL, '김범수','바둑'), (NULL,'김범수','축구'), (NULL,'조용필','축구'), (NULL,'은지원','축구'), (NULL,'은지원','봉사'), (NULL,'바비킴','봉사');
```
```
SELECT S.stdName, S.addr, SC.clubName, C.roomNo
FROM stdtbl S JOIN stdclubtbl SC
              ON S.stdName = SC.stdName
              JOIN clubtbl C
              ON SC.clubName = C.clubName 
ORDER BY S.stdName;
  
SELECT C.clubName, C.roomNo, S.stdName, S.addr
FROM  stdtbl S JOIN stdclubtbl SC
	           ON SC.stdName = S.stdName
               JOIN clubtbl C
               ON SC.clubName = C.clubName
ORDER BY C.clubName;
```

**22. UNION** 
- 두 쿼리결과를 합친다. 이때 두 쿼리결과의 컬럼 갯수/형식은 같아야 한다
```
select * from sqldb.stdtbl ;   ## --> stdname, addr 
select * from sqldb.clubtbl ;  ## --> clubname, roonNO
select * from sqldb.stdclubtbl ; ## --> num, stdname, clubname 

## union 
select *
from sqldb.stdtbl
union 
select * 
from sqldb.clubtbl ;
```

**23. IN, Not IN** 
```
## 전화번호가 없는(null)인 회원만 조회하기 
select username, concat(mobile1, mobile2) as 'Phone_NO' 
from sqldb.usertbl
where username in (
		select username 
        from sqldb.usertbl
        where mobile1 is null) 
; 
```
```
## 전화번호가 있는(not null)인 회원만 조회하기 
select username, concat(mobile1, mobile2) as 'Phone_NO' 
from sqldb.usertbl
where username not in (
		select username 
        from sqldb.usertbl
        where mobile1 is null) 
; 
```
 **24. IF and CASE** 
- 두 쿼리는 같은 결과를 출력한다. 
```
DROP PROCEDURE IF EXISTS IF_PROC_A ; 

DELIMITER $$ 
CREATE PROCEDURE IF_PROC_A() 
BEGIN 
	DECLARE POINT INT ; 
    DECLARE CREDIT CHAR(1) ; 
    SET POINT = 77 ; 
    
    IF POINT >= 90 THEN SET CREDIT = 'A' ; 
    ELSEIF POINT >= 80 THEN SET CREDIT = 'B' ; 
    ELSEIF POINT >= 70 THEN SET CREDIT = 'C' ; 
    ELSEIF POINT >= 60 THEN SET CREDIT = 'D' ; 
    ELSE SET CREDIT = 'F' ; 
    
    END IF ; 
    SELECT CONCAT('SCORE :', POINT), CONCAT('GRADE :', CREDIT) ; 
END $$ 
DELIMITER ; 

CALL IF_PROC_A();   ## Score :77  Grade :C
```
```
DROP PROCEDURE IF EXISTS IF_PROC_B ; 

DELIMITER $$ 
CREATE PROCEDURE IF_PROC_B() 
BEGIN 
	DECLARE POINT INT ; 
    DECLARE CREDIT CHAR(1) ; 
    SET POINT = 77 ; 
    
    CASE 
		WHEN POINT >= 90 THEN SET CREDIT = 'A' ; 
    WHEN POINT >= 80 THEN SET CREDIT = 'B' ; 
    WHEN POINT >= 70 THEN SET CREDIT = 'C' ; 
    WHEN POINT >= 60 THEN SET CREDIT = 'D' ; 
    ELSE SET CREDIT = 'F' ; 
    
    END CASE ; 
    SELECT CONCAT('SCORE :', POINT), CONCAT('GRADE :', CREDIT) ; 
END $$ 
DELIMITER ; 

CALL IF_PROC_B(); ## Score :77  Grade :C 
```
**26. While** 
- 1~100까지 모두 더하라 
```
DROP PROCEDURE IF EXISTS PROC_WHILE ; 

DELIMITER $$ 
CREATE PROCEDURE PROC_WHILE() 
BEGIN 
	DECLARE I INT ; 
    DECLARE K INT ; 
    
    SET I = 1 ; 
    SET K = 0 ; 
    
    WHILE (I <= 100) DO         
        SET K = K+i ; 
        SET I = I+1 ; 
	END WHILE ; 
	SELECT K; 
END $$
DELIMITER ;

CALL PROC_WHILE() ; ## 5050
```
