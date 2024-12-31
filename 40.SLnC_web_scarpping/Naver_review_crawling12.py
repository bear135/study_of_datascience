################################################################################################################################################
# Naver Place Customer Review Crawling code for SLNC 
# 제작: SCL 디지털기획팀 최영부 (2024. 12. 30) 
# parameter 1: user_specified_date ~ 크롤링 시작일자 지정, 해당날짜 이후의 데이터만 크롤링함  
# parameter 2: Convert reply date to datetime object (replied_date = None ... year_2 = 2024 ) ~ 당해년도 지정 
# 기타 : 네이버 플레이스의 구조는 부정기적으로 변경되며, 크롤링 전 변경사항 확인/코드수정 필요  
################################################################################################################################################

import time
import datetime
import requests
import re
from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlwings as xw
import pandas as pd
import warnings
import glob
import os

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 시작 시간 기록
start_time = time.time()

# 엑셀 파일 열기 (DRM 적용된 파일인 경우)
book = xw.Book('data/store_list.xlsx')
sheet = book.sheets[0]    
df = sheet.used_range.options(pd.DataFrame, index=False).value

###########################################################################################
################ 파라미터 지정 : 크롤링 시작일자, 당해년도
user_specified_date = "2024-12-01" 
this_year = 2024    
###########################################################################################

user_date = datetime.datetime.strptime(user_specified_date, '%Y-%m-%d')

# 각 매장에 대해 크롤링 수행
for x in range(len(df['store_name'])):
    url = df['store_url_naver'][x]
    s_brand = df['brand'][x]
    s_type = df['store_type'][x]
    s_store = df['store_name'][x]

    # 웹드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('--force-device-scale-factor=0.4')
    options.add_argument("disable-gpu")

    # 요청 설정
    session = requests.Session()
    headers = {"User-Agent": "user value"}
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # 새 엑셀 파일 설정
    now = datetime.datetime.now()
    xlsx = Workbook()
    list_sheet = xlsx.create_sheet('output')
    list_sheet.append(['brand', 'type', 'store', 'date', 'nickname', 'content', 'revisit', 'reply_txt', 'reply_date'])

    # 크롤링 시작
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(5)

        # 리뷰 데이터 수집
        continue_crawling = True
        while continue_crawling:
            # 페이지 스크롤
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)  # 1초 대기

            # "더보기" 버튼 클릭
            try:
                more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.fvwqf[role="button"]'))
                )
                more_button.click()
                time.sleep(2)  # 페이지 로딩 대기
            except Exception as e:
                print(f"Error clicking the 'More' button: {e}")
                break  # 더 이상 '더보기' 버튼이 없으면 반복 종료

            # 페이지에서 리뷰 정보 추출
            html = driver.page_source
            bs = BeautifulSoup(html, 'lxml')
            reviews = bs.select('li.pui__X35jYm.EjjAW')

            for r in reviews:
                ########################################################################################################################
                ################# 네이버 플레이스 웹페이지 구조 확인 요망 
                nickname = r.select_one('div.pui__JiVbY3 > span.pui__uslU0d')
                content = r.select_one('div.pui__vn15t2 a[role="button"]')
                review_date_element = r.select_one('div.pui__QKE5Pr > span.pui__gfuUIT > time[aria-hidden="true"]')
                revisit = r.select_one('div.pui__QKE5Pr > span:nth-of-type(2)')
                reply_date_element = r.select_one('div.pui__MzrP-X > span.pui__4APmFd > time[aria-hidden="true"]')
                reply_txt_element = r.select_one('div.pui__J0tczd > a[role="button"][data-pui-click-code="text"], div.pui__J0tczd > span[data-pui-click-code="text"]')
                ########################################################################################################################

                # 리뷰 날짜 추출 및 datetime 변환
                review_date_text = review_date_element.text if review_date_element else ''
                if review_date_text:
                    match = re.search(r'(\d{1,2})\.(\d{1,2})\.\w', review_date_text)
                    if match:
                        month, day = map(int, match.groups())
                        year = this_year  ## parameter 2 : 당해년도 지정
                        formatted_review_date = f'{year:04d}-{month:02d}-{day:02d}'
                        try:
                            review_date = datetime.datetime.strptime(formatted_review_date, '%Y-%m-%d')
                        except ValueError:
                            review_date = None
                    else:
                        review_date = None
                else:
                    review_date = None

                # review_date가 사용자 지정 날짜 이후인 경우에만 수집
                if review_date and review_date >= user_date:
                    # 리뷰 내용 및 답변 정보 추출
                    nickname_text = nickname.text if nickname else ''
                    content_text = content.text if content else ''
                    revisit_text = revisit.text if revisit else ''
                    reply_date_text = reply_date_element.text if reply_date_element else ''
                    reply_txt_text = reply_txt_element.text if reply_txt_element else ''

                    # 답변 날짜를 datetime 객체로 변환
                    replied_date = None
                    if reply_date_text:
                        match_2 = re.search(r'(\d{1,2})\.(\d{1,2})\.\w', reply_date_text)
                        if match_2:
                            month_2, day_2 = map(int, match_2.groups())
                            year_2 = this_year  ## parameter 2 : 당해년도 지정 
                            formatted_date_2 = f'{year_2:04d}-{month_2:02d}-{day_2:02d}'
                            replied_date = datetime.datetime.strptime(formatted_date_2, '%Y-%m-%d')

                    # 수집된 리뷰를 시트에 추가
                    list_sheet.append([s_brand, s_type, s_store, review_date, nickname_text, content_text, revisit_text, reply_txt_text, replied_date])
                    time.sleep(1)  # 다음 리뷰 대기

                # review_date가 사용자 지정 날짜 이전인 경우, 크롤링 종료
                elif review_date and review_date < user_date:
                    continue_crawling = False
                    break

        # 파일 저장
        file_name = f'naver_review_{s_store}.xlsx'
        xlsx.save(f'output/{file_name}')
        print(f"{s_store} finished")

    except Exception as e:
        print(e)
        file_name = f'naver_review_{s_store}.xlsx'
        xlsx.save(f'output/{file_name}')
        print(f"{s_store} finished with error")
    

# 엑셀 파일 병합
try:
    path = 'output/'
    files = glob.glob(path + "*.xlsx")
    excel = pd.DataFrame()
    for file_name in files:
        df = pd.read_excel(file_name, sheet_name='output')
        excel = pd.concat([excel, df], ignore_index=True)
    excel.to_excel('concated_file/naver_review_all.xlsx', index=False)
    print("All files merged successfully")
except Exception as ex:
    print(f'Error merging files: {ex}')


# 실행 시간 출력
end_time = time.time()
execution_time = (end_time - start_time) / 60
print("Execution time:", execution_time, "min")
