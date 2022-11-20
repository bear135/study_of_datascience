# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 08:14:46 2021

@author: zepur
"""


## 필요한 모듈 패키지 불러오기

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time, math, datetime, requests, json

pd.options.display.float_format = '{:,.2f}'.format # 소수점 2자리에서 반올림, 천단위 쉼표

## 발전실적 가져오는 클래스 output 정의

class output:

    def get_output(self, site, year, month, day):
    
        ## 키보드 설정

        self.ENTER = '/ue007'
        self.BACKSPACE = '/ue003'
        self.LEFT = '/ue012'
        self.UP = '/ue013'
        self.RIGHT ='/ue014'
        self.DOWN = '/ue015'

        ## 크롬을 이용해서 사이트 불러오기

        self.url = 'https://www.solarcube.co.kr/SrMain/SM010.aspx'
        self.driver = webdriver.Chrome('c:/코딩/python/chromedriver')
        self.driver.get(self.url)

        ## 사이트에서 원하는 정보 가져오기

        self.driver.find_element_by_xpath('//*[@id="Txt_1"]').send_keys('sclossolar')
        time.sleep(1.0)
        self.driver.find_element_by_xpath('//*[@id="Txt_2"]').send_keys('sclossolar')
        time.sleep(1.0)
        self.driver.find_element_by_xpath('//*[@id="imageField"]').click()
        time.sleep(1.0)
        self.driver.find_element_by_xpath('//*[@id="SrTop_Panel1"]/div[2]/ul/li[5]/a').click()
        time.sleep(1.0)
        self.driver.find_element_by_xpath('//*[@id="select2-SrTop_cbo_plant_d1-container"]').click()
        time.sleep(1.0)
        self.web1 = self.driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
        self.web1.send_keys('%s' % site)
        time.sleep(1.0)
        self.web1.send_keys(Keys.ENTER)
        time.sleep(1.0)
        self.web2 = self.driver.find_element_by_xpath('//*[@id="txt_Calendar"]')
        self.web2.click()
        time.sleep(1.0)
        for i in range(0,10):
            self.web2.send_keys(Keys.RIGHT)
        for i in range(0,10):
            self.web2.send_keys(Keys.BACKSPACE)
        self.web2.send_keys('%s-%s-%s' % (year, month, day))
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="submitbtn"]').click()
        time.sleep(1.0)

        ## 전체 내용 불러오기

        self.html = BeautifulSoup(self.driver.page_source, 'html.parser') # html 전체 내용 불러오기
        self.data = self.html.select('div.sub_contents > div.s_cont > table.sub_com_table > tbody > tr > td') # 발전실적 테이블 추출

        ## 크롬창 닫기

        self.driver.close()

        # 발전량 데이터 전처리 및 데이터프레임 만들기

        self.data_text = []

        for i in range(len(self.data)):
            self.a = str(self.data[i]).replace('<td>', '')
            self.b = self.a.replace('</td>', '')
            self.c = self.b.replace('<span class="f_w600">', '')
            self.d = self.c.replace('</span>', '')
            self.e = self.d.replace('<span class="align_C">', '')
            self.f = self.e.replace('<span class="align_R">', '')
            self.data_text.append(self.f)

        self.data_num = len(self.data_text) // 4

        self.data_array = np.array(self.data_text) # 리스트를 넘파이 어레이화
        self.data_array = self.data_array.reshape(int(self.data_num), 4) # nx4 행렬로 변환
        self.output_yesterday = pd.DataFrame(self.data_array, columns = ['site', 'date', 'output', 'radiation']) # 행렬을 데이터프레임으로 변환
        
        return self.output_yesterday

## 기상예보 클래스 forecast 정의

class forecast:
    
    # 기상 데이터 불러오기 함수 get_forecast() 정의

    def get_forecast(self, base_date, rows, base_time, nx, ny):
        self.servicekey = 'C5XWwKpv9QPJ8%2FX1nDI7qY2ZgVrDp9r4fzIXYCvjfj5uZ6MbPHY3SxTJkzrOpzDUrYW5j4%2FEJTklpG3JZzhigg%3D%3D'
        self.str = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?ServiceKey={servicekey}&pageNo={page}&numOfRows={rows}&dataType={data_type}&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}'
        self.url = self.str.format(servicekey=self.servicekey, page='1', rows=rows, data_type='json', base_date=base_date, base_time=base_time, nx=nx, ny=ny)
        self.resp = requests.get(self.url)
        self.data = json.loads(self.resp.text)
        return self.data

    # 불러온 데이터 정리하기 함수 make_df() 정의

    def make_forecast_df(self, data):
        self.data_items = data['response']['body']['items']['item']
        
        self.df_data = pd.DataFrame(self.data_items)
        self.df_data_sort = self.df_data.sort_values(by = 'category')

        # 예보항목 = ['TMP(온도)', 'WSD(풍속)', 'REH(습도)', 'SKY(운량)']

        self.TMP = self.df_data_sort.loc[self.df_data_sort.category == 'TMP', :]
        self.TMP= self.TMP.sort_index()
        self.TMP.columns = ['announce_date', 'announce_time', 'announce', 'forecast_date', 'forecast_time', 'temperature', 'x', 'y']
        #self.TMP = self.TMP.set_index('forecast_time')
        self.TMP = self.TMP.drop(['announce', 'x', 'y'], axis = 1)

        self.PCP = self.df_data_sort.loc[self.df_data_sort.category == 'PCP', :]
        self.PCP = self.PCP.sort_index()
        self.PCP = self.PCP.drop(['baseDate', 'baseTime', 'category', 'nx', 'ny'], axis = 1)
        self.PCP.columns = ['forecast_date', 'forecast_time', 'rainfall']
        self.PCP = self.PCP.set_index('forecast_time')
        self.PCP['rainfall'].replace('강수없음', '0', inplace = True)
        self.PCP['rainfall'].replace('1mm 미만', '0', inplace = True)
        self.PCP['rainfall'].replace('30~50mm', '40', inplace = True)
        self.PCP['rainfall'].replace('50mm 이상', '50', inplace = True)
        self.PCP['rainfall'] = self.PCP['rainfall'].str.replace('mm', '')
        self.PCP['rainfall'].astype('float64')
        self.forecast = pd.merge(self.TMP, self.PCP, how = 'left', on = ['forecast_time', 'forecast_date'])

        self.WSD = self.df_data_sort.loc[self.df_data_sort.category == 'WSD', :]
        self.WSD = self.WSD.sort_index()
        self.WSD = self.WSD.drop(['baseDate', 'baseTime', 'category', 'nx', 'ny'], axis = 1)
        self.WSD.columns = ['forecast_date', 'forecast_time', 'windvelocity']
        #self.WSD = self.WSD.set_index('forecast_time')
        self.forecast = pd.merge(self.forecast, self.WSD, how = 'left', on = ['forecast_time', 'forecast_date'])

        self.REH = self.df_data_sort.loc[self.df_data_sort.category == 'REH', :]
        self.REH = self.REH.sort_index()
        self.REH = self.REH.drop(['baseDate', 'baseTime', 'category', 'nx', 'ny'], axis = 1)
        self.REH.columns = ['forecast_date', 'forecast_time', 'humidity']
        #self.REH = self.REH.set_index('forecast_time')
        self.forecast = pd.merge(self.forecast, self.REH, how = 'left', on = ['forecast_time', 'forecast_date'])

        self.SNO = self.df_data_sort.loc[self.df_data_sort.category == 'SNO', :]
        self.SNO = self.SNO.sort_index()
        self.SNO = self.SNO.drop(['baseDate', 'baseTime', 'category', 'nx', 'ny'], axis = 1)
        self.SNO.columns = ['forecast_date', 'forecast_time', 'snowfall']
        self.SNO = self.SNO.set_index('forecast_time')
        self.SNO['snowfall'].replace('적설없음', '0', inplace = True)
        self.SNO['snowfall'].replace('1cm 미만', '0', inplace = True)
        self.SNO['snowfall'].replace('1cm미만', '0', inplace = True)
        self.SNO['snowfall'].replace('5cm 이상', '5', inplace = True)
        self.SNO['snowfall'].replace('5cm이상', '5', inplace = True)
        self.SNO['snowfall'] = self.SNO['snowfall'].str.replace('mm', '')
        self.SNO['snowfall'].astype('float64')
        self.forecast = pd.merge(self.forecast, self.SNO, how = 'left', on = ['forecast_time', 'forecast_date'])

        self.SKY = self.df_data_sort.loc[self.df_data_sort.category == 'SKY', :]
        self.SKY = self.SKY.sort_index()
        self.SKY = self.SKY.drop(['baseDate', 'baseTime', 'category', 'nx', 'ny'], axis = 1)
        self.SKY.columns = ['forecast_date', 'forecast_time', 'sky']
        #self.SKY = self.SKY.set_index('forecast_time')
        self.forecast = pd.merge(self.forecast, self.SKY, how = 'left', on = ['forecast_time', 'forecast_date'])
    
        return self.forecast

## 기상 데이터 클래스 weather 정의

class weather:
    
    # 기상 데이터 불러오기 함수 get_forecast() 정의

    def get_weather(self, rows, start_date, start_hour, end_date, end_hour, location):
        self.servicekey = 'C5XWwKpv9QPJ8%2FX1nDI7qY2ZgVrDp9r4fzIXYCvjfj5uZ6MbPHY3SxTJkzrOpzDUrYW5j4%2FEJTklpG3JZzhigg%3D%3D'
        self.str = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey={servicekey}&numOfRows={rows}&pageNo={page}&dataType={data_type}&dataCd=ASOS&dateCd=HR&stnIds={location}&endDt={end_date}&endHh={end_hour}&startHh={start_hour}&startDt={start_date}'
        self.url = self.str.format(servicekey=self.servicekey, page='1', rows=rows, data_type='json', start_date=start_date, start_hour=start_hour, end_date=end_date, end_hour=end_hour, location=location)
        self.resp = requests.get(self.url)
        self.data = json.loads(self.resp.text)
        return self.data

    # 불러온 데이터 정리하기 함수 make_weather_df() 정의
    
    def make_weather_df(self, data):
        self.data_items = data['response']['body']['items']['item']
        
        self.df_data = pd.DataFrame(self.data_items)
        self.weather_df = self.df_data.drop(['stnId', 'rnum', 'taQcflg', 'rnQcflg', 'wsQcflg', 'wd', 'wdQcflg', 'hmQcflg', 'pv', 'td', 'pa', 'paQcflg', 'ps', 'psQcflg', 'ss', 'ssQcflg', 'icsr', 'hr3Fhsc', 'dc10LmcsCa', 'clfmAbbrCd', 'lcsCh', 'vs', 'gndSttCd', 'dmstMtphNo', 'ts', 'tsQcflg', 'm005Te', 'm01Te', 'm02Te', 'm03Te'], axis = 1)
        self.weather_df.columns = ['date', 'location', 'temperature', 'rainfall', 'windvelocity', 'humidity', 'snowfall', 'sky']
        return self.weather_df

## 날짜 구하는 함수 thedaybefore(), yesterday(), today(), tomorrow() 정의
    
def thedaybefore():
    cdate = datetime.datetime.today()
    pdate = cdate - datetime.timedelta(days = 2)
    p_year = str(pdate.strftime("%y"))
    p_month = str(pdate.strftime("%m"))
    p_day = str(pdate.strftime("%d"))
    thedaybefore = '20' + p_year + p_month + p_day
        
    return thedaybefore

def yesterday():
    cdate = datetime.datetime.today()
    pdate = cdate - datetime.timedelta(days = 1)
    p_year = str(pdate.strftime("%y"))
    p_month = str(pdate.strftime("%m"))
    p_day = str(pdate.strftime("%d"))
    yesterday = '20' + p_year + p_month + p_day
        
    return yesterday

def today():

    cdate = datetime.datetime.today()
    year = str(cdate.strftime("%y"))
    month = str(cdate.strftime("%m"))
    day = str(cdate.strftime("%d"))
    today = '20' + year + month + day
    
    return today

def tomorrow():
    
    cdate = datetime.datetime.today()
    ndate = cdate + datetime.timedelta(days = 1)
    n_year = str(ndate.strftime("%y"))
    n_month = str(ndate.strftime("%m"))
    n_day = str(ndate.strftime("%d"))
    tomorrow = '20' + n_year + n_month + n_day
    
    return tomorrow

## 태양위치 구하는 함수 solar() 정의

def solar(local_latitude, local_longitude, standard_longitude, start_day):
    
    # 각도 단위 변경

    d2r = math.pi / 180
    r2d = 180 / math.pi
    
    date = []
    hour = []
    altitude = []
    altitude_before = []
    azimuth = []
    azimuth_2 = []
    azimuth_2_before = []
    azimuth_final = []

    for i in range(0, int(n_hours)):
    
    
        # 계산 시각
        
        cal_day = start_day + datetime.timedelta(hours = i)
        year = int(cal_day.strftime("%y"))
        month = int(cal_day.strftime("%m"))
        day = int(cal_day.strftime("%d"))
        local_hour = int(cal_day.strftime("%H"))
        local_min = int(cal_day.strftime("%M"))
    
        date.append(int('20' + cal_day.strftime("%y%m%d%H%M")))
        hour.append(int(local_hour))        
        
        # 계산 시각 -1 시간

        cal_day_before = start_day + datetime.timedelta(hours = i - 1)
        year_before = int(cal_day_before.strftime("%y"))
        month_before = int(cal_day_before.strftime("%m"))
        day_before = int(cal_day_before.strftime("%d"))
        local_hour_before = int(cal_day_before.strftime("%H"))
        local_min_before = int(cal_day_before.strftime("%M"))

        # 균시차

        day_of_year = datetime.datetime(year, month, day).timetuple().tm_yday
        B = (day_of_year - 1) * 360 / 365
        EOT = 229.2 * (0.000075
                       + 0.001868 * math.cos(d2r * B)
                       - 0.032077 * math.sin(d2r * B)
                       - 0.014615 * math.cos(d2r * 2 * B)
                       - 0.04089 * math.sin(d2r * 2 * B))

        day_of_year_before = datetime.datetime(year_before, month_before, day_before).timetuple().tm_yday
        B_before = (day_of_year_before - 1) * 360 / 365
        EOT_before = 229.2 * (0.000075
                       + 0.001868 * math.cos(d2r * B_before)
                       - 0.032077 * math.sin(d2r * B_before)
                       - 0.014615 * math.cos(d2r * 2 * B_before)
                       - 0.04089 * math.sin(d2r * 2 * B_before))

        # 시간각

        local_hour_decimal = local_hour + local_min / 60
        delta_longitude = local_longitude - standard_longitude
        solar_time_decimal = (local_hour_decimal * 60 + 4 + delta_longitude + EOT) / 60
        solar_time_hour = int(solar_time_decimal)
        solar_time_min = (solar_time_decimal * 60) % 60
        hour_angle = (local_hour_decimal * 60 + 4 * delta_longitude + EOT) / 60 * 15 - 180

        local_hour_decimal_before = local_hour_before + local_min_before / 60
        delta_longitude = local_longitude - standard_longitude
        solar_time_decimal_before = (local_hour_decimal_before * 60 + 4 + delta_longitude + EOT_before) / 60
        solar_time_hour_before = int(solar_time_decimal_before)
        solar_time_min_before = (solar_time_decimal_before * 60) % 60
        hour_angle_before = (local_hour_decimal_before * 60 + 4 * delta_longitude + EOT_before) / 60 * 15 - 180

        # 적위

        solar_declination = 23.45 * math.sin(d2r * 360 / 365 * (284 + day_of_year))
        
        solar_declination_before = 23.45 * math.sin(d2r * 360 / 365 * (284 + day_of_year_before))

        # 태양 고도

        term_1 = math.cos(d2r * local_latitude) * math.cos(d2r * solar_declination) * math.cos(d2r * hour_angle) + math.sin(d2r * local_latitude) * math.sin(d2r * solar_declination)
        solar_altitude = r2d * math.asin(term_1)
        altitude.append(solar_altitude)
        
        term_1_before = math.cos(d2r * local_latitude) * math.cos(d2r * solar_declination_before) * math.cos(d2r * hour_angle_before) + math.sin(d2r * local_latitude) * math.sin(d2r * solar_declination_before)
        solar_altitude_before = r2d * math.asin(term_1_before)
        altitude_before.append(solar_altitude_before)

        # 태양 방위각 1

        term_2 = (math.sin(d2r * solar_altitude) * math.sin(d2r * local_latitude)- math.sin(d2r * solar_declination)) / (math.cos(d2r * solar_altitude) * math.cos(d2r * local_latitude))
        solar_azimuth = r2d * math.acos(term_2)
        azimuth.append(solar_azimuth)
        
        # Solar Zenith Angle
        
        solar_zenith_angle = r2d * math.acos(math.sin(d2r * local_latitude) * math.sin(d2r * solar_declination) + math.cos(d2r * local_latitude) * math.cos(d2r * solar_declination) * math.cos(d2r * hour_angle))

        solar_zenith_angle_before = r2d * math.acos(math.sin(d2r * local_latitude) * math.sin(d2r * solar_declination_before) + math.cos(d2r * local_latitude) * math.cos(d2r * solar_declination_before) * math.cos(d2r * hour_angle_before))
    
        # 태양 방위각 2
    
        term_3 = (math.sin(d2r * solar_declination) * math.cos(d2r * local_latitude) - math.cos(d2r * hour_angle) * math.cos(d2r * solar_declination) * math.sin(d2r * local_latitude)) / math.sin(d2r * solar_zenith_angle)
        solar_azimuth_2 = r2d * math.acos(term_3)
        azimuth_2.append(solar_azimuth_2)
        
        term_3_before = (math.sin(d2r * solar_declination_before) * math.cos(d2r * local_latitude) - math.cos(d2r * hour_angle_before) * math.cos(d2r * solar_declination_before) * math.sin(d2r * local_latitude)) / math.sin(d2r * solar_zenith_angle_before)
        solar_azimuth_2_before = r2d * math.acos(term_3_before)
        azimuth_2_before.append(solar_azimuth_2_before)
        
        azimuth_delta = solar_azimuth_2 - solar_azimuth_2_before

        if azimuth_delta <= 0:
            solar_azimuth_final = 360 - solar_azimuth_2
        else:
            solar_azimuth_final = solar_azimuth_2
        
        azimuth_final.append(solar_azimuth_final)
    
    solar = pd.DataFrame(date)
    solar['hour'] = hour
    solar['altitude'] = altitude
    solar['altitude_before'] = altitude_before
    solar['altitude_change'] = solar['altitude'] - solar['altitude_before']
    solar['azimuth'] = azimuth_final
    solar = solar.drop(['altitude_before'], axis = 1)
    
    return solar

## 기계학습 모델(KernelSVR) 정의
    
def make_predict_model(data, C):

    # 예측 데이터를 학습, 테스트 데이터로 나누기

    X_train, X_test, Y_train, Y_test = train_test_split(data.drop('output', axis = 1), data['output'], test_size = 0.01, random_state = 0, shuffle = 'FALSE')
    # X_train = X_train.values
    # Y_train = Y_train.values
    sc = StandardScaler()
    X_train_st = sc.fit_transform(X_train)
    
    # 모델 정의
    
    model = SVR(kernel = 'rbf', C = C, gamma = 'scale')
    model.fit(X_train_st, Y_train)

    # 모델 정확도 생성

    model_score = model.score(X_train_st, Y_train)
    print('\n')
    print('<%s>'% site)
    print('%s 발전량 예측 머신러닝모델 정확도 :'% site, round(model_score * 100, 2), '%')
    
    return model, sc

## 사이트 합계 구하는 함수 site_sum() 정의

def site_sum(stage):
    
    # 사이트 정의
    
    site = ['osan', 'kwangmyoung']
    capacity = [146.52, 173.4]
    
    # 용량 합계 구하기
    
    capacity_sum = 0

    for k in capacity:
        capacity_sum = capacity_sum + k
    
    # 어제 날짜 구하기
    
    cdate = datetime.datetime.today()
    pdate = cdate - datetime.timedelta(days = 1)
    p_year = str(pdate.strftime("%y"))
    p_month = str(pdate.strftime("%m"))
    p_day = str(pdate.strftime("%d"))
    yesterday = '20' + p_year + p_month + p_day
    
    # -그래프 표현에 필요한 변수 정의

    graph_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    # 사이트별 결과 파일 불러오기
    
    output_f = pd.DataFrame()
    output = pd.DataFrame()
    model_check = pd.DataFrame()

    for i in site:
        globals()['result_' + str(i)] = pd.read_csv("result/data/%s/%s_result_%s(%s).csv" % (i, i, stage, yesterday), encoding = 'cp949')
        output_f = pd.concat([output_f, globals()['result_' + str(i)]['output_f']], axis = 1)
        output = pd.concat([output, globals()['result_' + str(i)]['output']], axis = 1)
        model_check = pd.concat([model_check, globals()['result_' + str(i)]['model_check']], axis = 1)
    
    # 사이트별 결과 합계 구하기
    
    output_f['sum'] = output_f.sum(axis = 1)
    output['sum'] = output.sum(axis = 1)
    model_check['sum'] = model_check.sum(axis = 1)
    
    # 오차 및 오차율 구하기

    result = pd.DataFrame()
    result['hour'] = result_osan.loc[:, 'hour']
    result['date'] = result_osan.loc[:, 'date']
    result['output_f'] = output_f.loc[:, 'sum']
    result['output'] = output.loc[:, 'sum']
    result['model_check'] = model_check.loc[:, 'sum']
    result['error_output'] = result['output_f'] - result['output']
    result['error_model_check'] = result['model_check'] - result['output']
    result['output_error_rate'] = result['error_output'] / capacity_sum * 100
    result['model_check_error_rate'] = result['error_model_check'] / capacity_sum * 100
    result['output_error_rate'].fillna(0, inplace = True)
    result['model_check_error_rate'].fillna(0, inplace = True)

    # 인센티브 계산

    incentive_data = result.loc[result.output >= (capacity_sum / 10), :]
    incentive_cal_data = list(incentive_data.loc[:, 'output_error_rate'])
    incentive_cal_check = list(incentive_data.loc[:, 'model_check_error_rate'])
    incentive_cal_hour = list(incentive_data.loc[:, 'hour'])
    error_data = pd.DataFrame([incentive_cal_hour, incentive_cal_data, incentive_cal_check]).transpose()
    error_data.columns = ['time', 'predict_error_rate', 'model_error_rate']
    incentive_price_list = []
    for t in incentive_cal_data:
        if -6 <= t <= 6:
            incentive_price = 4
        elif -8 <= t <= 8:
            incentive_price = 3
        else:
            incentive_price = 0
        incentive_price_list.append(incentive_price)
    incentive = pd.DataFrame(incentive_cal_hour, columns = ['hour'])
    incentive['incentive_price'] = incentive_price_list
    result = pd.merge(result, incentive, how = 'left', on = ['hour'])
    result['incentive_price'].fillna(0, inplace = True)
    result['incentive'] = result['output'] * result['incentive_price']
    result['incentive'].fillna(0, inplace = True)
    
    # 분석 결과 그래프 그리기
    
    plt.plot(graph_hours, result['output_f'], label = 'predictive value')
    plt.plot(graph_hours, result['output'], label = 'result value')
    plt.plot(graph_hours, result['model_check'], label = 'model check', color = 'grey', linestyle = 'dashed')
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('output (kWh)')
    plt.xticks(graph_hours)
    plt.title('%s Result Analysis (%s)'% (stage,yesterday))
    print('\n')
    print('<어제 사이트 실적 합계>')
    print('=============================================')
    print('어제 %s 실적 합계 분석' % stage)
    print('=============================================')
    print('%s 예측 오차율' % stage)
    print(error_data)
    print('---------------------------------------------')
    print('%s 예측 인센티브 : ' % stage, round(result['incentive'].sum(), 2), "원")
    plt.savefig('result/graph/sum/sum_result_%s(%s).png'% (stage, yesterday), bbox_inches = 'tight', figsize = (10,5), dpi = 300)
    plt.show()
    print('=============================================')
    
    # 분석 결과 파일로 내보내기

    result.to_csv('result/data/sum/sum_result_%s(%s).csv'% (stage, yesterday), encoding = 'cp949')
    
    return result

## 예측에 필요한 변수 정의

    # 사이트 리스트 [name, site, capacity, local_latitude, local_longitude, nx, ny, location]
    
# osan = {'name' : 'osan', 'site' : '오산 삼천리 연구소', 'capacity' : 146.52, 'local_latitude' : 37.18301208, 'local_longitude' : 127.0320559, 'nx' : 61, 'ny' : 118}
# kwangmyoung = {'name' : 'kwangmyoung', 'site' : '삼천리 광명열병합사업단', 'capacity' : 173.4, 'local_latitude' : 37.422222, 'local_longitude' : 126.8910605, 'nx' : 58, 'ny' : 124}

site_list = [['osan', '오산 삼천리 연구소', 146.52, 37.18301208, 127.0320559, 61, 118, 119],
             ['kwangmyoung', '삼천리 광명열병합사업단', 173.4, 37.422222, 126.8910605, 58, 124, 119]]

    # 서포트벡터머신 C값 입력

C = int(input('서포트벡터머신의 C값을 입력하세요 (예 : 200) : '))

    # 기계학습 학습데이터 기간(년수)

train_year_period = int(input('학습 기간을 입력하세요 (년) : '))

    #  어제 실적 정리 여부 질문

progress = input('어제 예측결과 정확도를 분석하시겠습니까? (Y/N) : ')

    # 사이트 합계 구하기 여부 질문

sum_choice = input('어제 사이트 실적 합계를 구하시겠습니까? (Y/N) : ')

    # 발전실적 가져오는데 필요한 날짜, 시간

yesterday = yesterday()
today = today()
tomorrow = tomorrow()
rows = 500
base_time_1st = "0800"
base_time_2nd = "1400"

    # -기상 데이터 가져오는데 필요한 날짜, 시간

start_date = yesterday
start_hour = '00'
end_date = yesterday
end_hour = '23'

    # -태양위치 가져오는데 필요한 날짜, 시간

date_today = datetime.datetime.today()
hour_today = int(date_today.strftime('%H'))

date_tomorrow = date_today + datetime.timedelta(days = 1)
year_tomorrow = int('20' + date_tomorrow.strftime('%y'))
month_tomorrow = int(date_tomorrow.strftime('%m'))
day_tomorrow = int(date_tomorrow.strftime('%d'))

    # -발전실적 가져오는데 필요한 날짜, 시간

date_yesterday = date_today - datetime.timedelta(days = 1)
year_yesterday = '20' + date_yesterday.strftime('%y')
month_yesterday = date_yesterday.strftime('%m')
day_yesterday = date_yesterday.strftime('%d')


s_year = year_tomorrow
s_month = month_tomorrow
s_day = day_tomorrow
s_local_hour = 0
s_local_min = 0

e_year = year_tomorrow
e_month = month_tomorrow
e_day = day_tomorrow
e_local_hour = 23
e_local_min = 0

start_day = datetime.datetime(s_year, s_month, s_day)
end_day = datetime.datetime(e_year, e_month, e_day)

n = start_day - end_day
n_hours = - n.total_seconds() / 3600 + 24

    # -그래프 표현에 필요한 변수 정의

graph_hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

## 발전량 예측 모델 생성

    # -예측 사이트 선택

for site_sq in range(0, len(site_list)):
    name = site_list[site_sq][0]
    site = site_list[site_sq][1]
    capacity = site_list[site_sq][2]
    local_latitude = site_list[site_sq][3]
    local_longitude = site_list[site_sq][4]
    nx = site_list[site_sq][5]
    ny = site_list[site_sq][6]
    location = site_list[site_sq][7]
    standard_longitude = 135

    # -학습데이터 불러오기 및 전처리

    data_train = pd.read_csv("%s_train_data.csv" % name)

    data_train['temperature'].fillna(0., inplace = True)
    data_train['rainfall'].fillna(0., inplace = True)
    data_train['windvelocity'].fillna(0., inplace = True)
    data_train['humidity'].fillna(0., inplace = True)
    data_train['snowfall'].fillna(0., inplace = True)
    data_train['sky'].fillna(0., inplace = True)
    data_train['output'].fillna(0., inplace = True)
    data_train = data_train.astype({'output' : 'int'}) # 분류모델이기 때문에 데이터 형을 int로 변환

    rows_df = len(data_train)
    data_train.drop(data_train.index[0:rows_df - 8760 * train_year_period], inplace = True)

    # -학습 시행

    model, sc = make_predict_model(data_train, C)
    
    ## -어제 실적 정리

    if progress == 'N':
        pass
    else:

        ## 어제 발전실적 가져오기

        g_output = output()
        g_output_yesterday = g_output.get_output(site, year_yesterday, month_yesterday, day_yesterday)

        ## 어제 기상데이터 가져오기 및 전운량 데이터(10분위)를 4분위로 변경

        g_weather = weather()
        weather_yesterday = g_weather.get_weather(rows, start_date, start_hour, end_date, end_hour, location)
        weather_yesterday_df = g_weather.make_weather_df(weather_yesterday)
        #weather_yesterday_df['date'] = pd.to_datetime(weather_yesterday_df['date'])
        #weather_yesterday_df['hour'] = weather_yesterday_df['date'].dt.hour
        #weather_yesterday_df['hour'] = weather_yesterday_df['hour'].astype(int)
        #index_hour = pd.DataFrame(graph_hours, columns = ['hour'])
        #weather_yesterday_df = pd.merge(index_hour, weather_yesterday_df, how = 'left', on = ['hour'])
        #weather_yesterday_df['date'] = weather_yesterday_df['date'].fillna('2022-03-01 00:00:00')
        #weather_yesterday_df['date'] = pd.to_datetime(weather_yesterday_df['date'])
        #weather_yesterday_df = weather_yesterday_df.fillna(0)
        weather_yesterday_df['hour'] = graph_hours
        weather_yesterday_df['sky'].replace('', 0, inplace = True)
        sky_yesterday = list(weather_yesterday_df.loc[:,'sky'])
        sky_yesterday_modified = []
        for k in sky_yesterday:
            if 0 <= int(k) <= 2:
                sky = 1
            elif 3 <= int(k) <= 5:
                sky = 2
            elif 6 <= int(k) <= 8:
                sky = 3
            else:
                sky = 4
            sky_yesterday_modified.append(sky)
        weather_yesterday_df['sky_modified'] = sky_yesterday_modified

        ## 어제 예측 데이터 가져오기

        predict_result_yesterday_1st = pd.read_csv("predict/data/%s/%s_predict_1st(%s).csv" % (name, name, yesterday))
        predict_result_yesterday_2nd = pd.read_csv("predict/data/%s/%s_predict_2nd(%s).csv" % (name, name, yesterday))
        predict_result_yesterday_1st = predict_result_yesterday_1st.drop('Unnamed: 0', axis = 1)
        predict_result_yesterday_2nd = predict_result_yesterday_2nd.drop('Unnamed: 0', axis = 1)
        predict_result_yesterday_1st.columns = ['hour', 'altitude', 'altitude_change', 'azimuth', 'temperature_f', 'rainfall_f', 'windvelocity_f', 'humidity_f', 'snowfall_f', 'sky_f', 'output_f']
        predict_result_yesterday_2nd.columns = ['hour', 'altitude', 'altitude_change', 'azimuth', 'temperature_f', 'rainfall_f', 'windvelocity_f', 'humidity_f', 'snowfall_f', 'sky_f', 'output_f']

        ## 어제 실적 정리

        # - 실적 데이터 합치기 (발전량예측 + 발전실적 + 기상데이터)
    
        result_yesterday_1st = pd.merge(predict_result_yesterday_1st, weather_yesterday_df, how = 'left', on = ['hour'])
        result_yesterday_2nd = pd.merge(predict_result_yesterday_2nd, weather_yesterday_df, how = 'left', on = ['hour'])
        #result_yesterday_1st['date'] = pd.to_datetime(result_yesterday_1st['date'])
        #result_yesterday_2nd['date'] = pd.to_datetime(result_yesterday_2nd['date'])
        #g_output_yesterday['date'] = pd.to_datetime(g_output_yesterday['date'])
        result_yesterday_1st = pd.merge(result_yesterday_1st, g_output_yesterday, how = 'left', on = ['date'])
        result_yesterday_2nd = pd.merge(result_yesterday_2nd, g_output_yesterday, how = 'left', on = ['date'])
        result_yesterday_1st['site'].fillna(site, inplace = True)
        result_yesterday_1st['output'].fillna(0, inplace = True)
        result_yesterday_1st['radiation'].fillna(0, inplace = True)
        result_yesterday_2nd['site'].fillna(site, inplace = True)
        result_yesterday_2nd['output'].fillna(0, inplace = True)
        result_yesterday_2nd['radiation'].fillna(0, inplace = True)
    
        # - 데이터 형 변경 (object -> float)
    
        result_yesterday_1st['output'] = pd.to_numeric(list(result_yesterday_1st.output))
        result_yesterday_2nd['output'] = pd.to_numeric(list(result_yesterday_1st.output))
        result_yesterday_1st['temperature'] = pd.to_numeric(list(result_yesterday_1st.temperature))
        result_yesterday_2nd['temperature'] = pd.to_numeric(list(result_yesterday_1st.temperature))
        result_yesterday_1st['rainfall'] = pd.to_numeric(list(result_yesterday_1st.rainfall))
        result_yesterday_2nd['rainfall'] = pd.to_numeric(list(result_yesterday_1st.rainfall))
        result_yesterday_1st['windvelocity'] = pd.to_numeric(list(result_yesterday_1st.windvelocity))
        result_yesterday_2nd['windvelocity'] = pd.to_numeric(list(result_yesterday_1st.windvelocity))
        result_yesterday_1st['humidity'] = pd.to_numeric(list(result_yesterday_1st.humidity))
        result_yesterday_2nd['humidity'] = pd.to_numeric(list(result_yesterday_1st.humidity))
        result_yesterday_1st['snowfall'] = pd.to_numeric(list(result_yesterday_1st.snowfall))
        result_yesterday_2nd['snowfall'] = pd.to_numeric(list(result_yesterday_1st.snowfall))
        result_yesterday_1st['sky'] = pd.to_numeric(list(result_yesterday_1st.sky))
        result_yesterday_2nd['sky'] = pd.to_numeric(list(result_yesterday_1st.sky))
        
        # - 결측치 처리
        
        result_yesterday_1st['temperature'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_2nd['temperature'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_1st['windvelocity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_2nd['windvelocity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_1st['humidity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_2nd['humidity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_1st['sky'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_2nd['sky'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        result_yesterday_1st['rainfall'].fillna(0, inplace = True)
        result_yesterday_1st['snowfall'].fillna(0, inplace = True)
        result_yesterday_2nd['rainfall'].fillna(0, inplace = True)
        result_yesterday_2nd['snowfall'].fillna(0, inplace = True)
    
        # - 모델 검증 데이터 만들기
    
        result_yesterday_check_1st_data = result_yesterday_1st.drop(['temperature_f', 'rainfall_f', 'windvelocity_f', 'humidity_f', 'snowfall_f', 'sky_f', 'output_f', 'date', 'location', 'sky', 'site', 'output', 'radiation'], axis = 1)
        result_yesterday_check_2nd_data = result_yesterday_2nd.drop(['temperature_f', 'rainfall_f', 'windvelocity_f', 'humidity_f', 'snowfall_f', 'sky_f', 'output_f', 'date', 'location', 'sky', 'site', 'output', 'radiation'], axis = 1)
    
        # - 모델 검증 시행
    
        result_yesterday_check_1st_data_st = sc.transform(result_yesterday_check_1st_data)
        result_yesterday_check_1st = model.predict(result_yesterday_check_1st_data_st)
    
        result_yesterday_check_2nd_data_st = sc.transform(result_yesterday_check_2nd_data)
        result_yesterday_check_2nd = model.predict(result_yesterday_check_2nd_data_st)
    
        result_yesterday_1st['model_check'] = result_yesterday_check_1st
        result_yesterday_2nd['model_check'] = result_yesterday_check_2nd
    
        # - 오차 계산
    
        result_yesterday_1st['error_temperature'] = result_yesterday_1st['temperature_f'] - result_yesterday_1st['temperature']
        result_yesterday_2nd['error_temperature'] = result_yesterday_2nd['temperature_f'] - result_yesterday_2nd['temperature']
        result_yesterday_1st['error_rainfall'] = result_yesterday_1st['rainfall_f'] - result_yesterday_1st['rainfall']
        result_yesterday_2nd['error_rainfall'] = result_yesterday_2nd['rainfall_f'] - result_yesterday_2nd['rainfall']
        result_yesterday_1st['error_windvelocity'] = result_yesterday_1st['windvelocity_f'] - result_yesterday_1st['windvelocity']
        result_yesterday_2nd['error_windvelocity'] = result_yesterday_2nd['windvelocity_f'] - result_yesterday_2nd['windvelocity']
        result_yesterday_1st['error_humidity'] = result_yesterday_1st['humidity_f'] - result_yesterday_1st['humidity']
        result_yesterday_2nd['error_humidity'] = result_yesterday_2nd['humidity_f'] - result_yesterday_2nd['humidity']
        result_yesterday_1st['error_snowfall'] = result_yesterday_1st['snowfall_f'] - result_yesterday_1st['snowfall']
        result_yesterday_2nd['error_snowfall'] = result_yesterday_2nd['snowfall_f'] - result_yesterday_2nd['snowfall']
        result_yesterday_1st['error_sky'] = result_yesterday_1st['sky_f'] - result_yesterday_1st['sky_modified']
        result_yesterday_2nd['error_sky'] = result_yesterday_2nd['sky_f'] - result_yesterday_2nd['sky_modified']
        result_yesterday_1st['error_output'] = result_yesterday_1st['output_f'] - result_yesterday_1st['output']
        result_yesterday_2nd['error_output'] = result_yesterday_2nd['output_f'] - result_yesterday_2nd['output']
        result_yesterday_1st['error_model_check'] = result_yesterday_1st['model_check'] - result_yesterday_1st['output']
        result_yesterday_2nd['error_model_check'] = result_yesterday_2nd['model_check'] - result_yesterday_2nd['output']

        # 정확도 계산
    
        result_yesterday_1st['output_error_rate'] = (result_yesterday_1st['error_output'] / capacity * 100)
        result_yesterday_2nd['output_error_rate'] = (result_yesterday_2nd['error_output'] / capacity * 100)
        result_yesterday_1st['output_error_rate'].fillna(0, inplace = True)
        result_yesterday_2nd['output_error_rate'].fillna(0, inplace = True)
    
        result_yesterday_1st['model_check_error_rate'] = (result_yesterday_1st['error_model_check'] / capacity * 100)
        result_yesterday_2nd['model_check_error_rate'] = (result_yesterday_2nd['error_model_check'] / capacity * 100)
        result_yesterday_1st['model_check_error_rate'].fillna(0, inplace = True)
        np.nan_to_num(result_yesterday_1st['model_check_error_rate'], copy = False)
        result_yesterday_2nd['model_check_error_rate'].fillna(0, inplace = True)
        np.nan_to_num(result_yesterday_2nd['model_check_error_rate'], copy = False)
    
        # 인센티브 계산
    
        incentive_data_1st = result_yesterday_1st.loc[result_yesterday_1st.output >= (capacity / 10), :]
        incentive_cal_data_1st = list(incentive_data_1st.loc[:, 'output_error_rate'])
        incentive_cal_check_1st = list(incentive_data_1st.loc[:, 'model_check_error_rate'])
        incentive_cal_hour_1st = list(incentive_data_1st.loc[:, 'hour'])
        error_data_1st = pd.DataFrame([incentive_cal_hour_1st, incentive_cal_data_1st, incentive_cal_check_1st]).transpose()
        error_data_1st.columns = ['time', 'predict_error_rate', 'model_error_rate']
        incentive_price_list_1st = []
        for t in incentive_cal_data_1st:
            if -6 <= t <= 6:
                incentive_price_1st = 4
            elif -8 <= t <= 8:
                incentive_price_1st = 3
            else:
                incentive_price_1st = 0
            incentive_price_list_1st.append(incentive_price_1st)
        incentive_1st = pd.DataFrame(incentive_cal_hour_1st, columns = ['hour'])
        incentive_1st['incentive_price'] = incentive_price_list_1st
        result_yesterday_1st = pd.merge(result_yesterday_1st, incentive_1st, how = 'left', on = ['hour'])
        result_yesterday_1st['incentive_price'].fillna(0, inplace = True)
        result_yesterday_1st['incentive'] = result_yesterday_1st['output'] * result_yesterday_1st['incentive_price']
        result_yesterday_1st['incentive'].fillna(0, inplace = True)

        incentive_data_2nd = result_yesterday_2nd.loc[result_yesterday_2nd.output >= (capacity / 10), :]
        incentive_cal_data_2nd = list(incentive_data_2nd.loc[:, 'output_error_rate'])
        incentive_cal_check_2nd = list(incentive_data_2nd.loc[:, 'model_check_error_rate'])
        incentive_cal_hour_2nd = list(incentive_data_2nd.loc[:, 'hour'])
        error_data_2nd = pd.DataFrame([incentive_cal_hour_2nd, incentive_cal_data_2nd, incentive_cal_check_2nd]).transpose()
        error_data_2nd.columns = ['time', 'predict_error_rate', 'model_error_rate']
        incentive_price_list_2nd = []
        for s in incentive_cal_data_2nd:
            if -6 <= s <= 6:
                incentive_price_2nd = 4
            elif -8 <= s <= 8:
                incentive_price_2nd = 3
            else:
                incentive_price_2nd = 0
            incentive_price_list_2nd.append(incentive_price_2nd)
        incentive_2nd = pd.DataFrame(incentive_cal_hour_2nd, columns = ['hour'])
        incentive_2nd['incentive_price'] = incentive_price_list_2nd
        result_yesterday_2nd = pd.merge(result_yesterday_2nd, incentive_2nd, how = 'left', on = ['hour'])
        result_yesterday_2nd['incentive_price'].fillna(0, inplace = True)
        result_yesterday_2nd['incentive'] = result_yesterday_2nd['output'] * result_yesterday_1st['incentive_price']
        result_yesterday_2nd['incentive_price'].fillna(0, inplace = True)
    
        # 분석 결과 그래프 그리기
    
        plt.plot(graph_hours, result_yesterday_1st['output_f'], label = 'predictive value')
        plt.plot(graph_hours, result_yesterday_1st['output'], label = 'result value')
        plt.plot(graph_hours, result_yesterday_1st['model_check'], label = 'model check', color = 'grey', linestyle = 'dashed')
        plt.legend()
        plt.xlabel('time')
        plt.ylabel('output (kWh)')
        plt.xticks(graph_hours)
        plt.title('1st Result Analysis (%s)'% yesterday)
        print('=============================================')
        print('%s 어제 1차 실적 분석'% site)
        print('=============================================')
        print('%s 1차 예측 오차율'% site)
        print(error_data_1st)
        print('---------------------------------------------')
        print('1차 예측 인센티브 : ', result_yesterday_1st['incentive'].sum(), "원")
        plt.savefig('result/graph/%s/%s_result_1st(%s).png'% (name, name, yesterday), bbox_inches = 'tight', figsize = (10,5), dpi = 300)
        plt.show()
        print('=============================================')
    
        plt.plot(graph_hours, result_yesterday_2nd['output_f'], label = 'predictive value')
        plt.plot(graph_hours, result_yesterday_2nd['output'], label = 'result value')
        plt.plot(graph_hours, result_yesterday_2nd['model_check'], label = 'model check', color = 'grey', linestyle = 'dashed')
        plt.legend()
        plt.xlabel('time')
        plt.ylabel('output (kWh)')
        plt.xticks(graph_hours)
        plt.title('2nd Result Analysis (%s)'% yesterday)
        print('=============================================')
        print('%s 어제 2차 실적 분석'% site)
        print('=============================================')
        print('%s 2차 예측 오차율'% site)
        print(error_data_2nd)
        print('---------------------------------------------')
        print('2차 예측 인센티브 : ', result_yesterday_2nd['incentive'].sum(), "원")
        plt.savefig('result/graph/%s/%s_result_2nd(%s).png'% (name, name, yesterday), bbox_inches = 'tight', figsize = (10,5), dpi = 300)
        plt.show()
        print('=============================================')
    
        # 분석 결과 파일로 내보내기

        result_yesterday_1st.to_csv('result/data/%s/%s_result_1st(%s).csv'% (name, name, yesterday), encoding = 'cp949')
        result_yesterday_2nd.to_csv('result/data/%s/%s_result_2nd(%s).csv'% (name, name, yesterday), encoding = 'cp949')
        
    ## 태양 위치 계산

    solar_altitude = solar(local_latitude, local_longitude, standard_longitude, start_day)
    solar_altitude.columns = ['date', 'hour', 'altitude', 'altitude_change', 'azimuth']

    ## 1차 예측 시행

    if hour_today * 100 < int(base_time_1st):
        pass
    else:

        # -1차 기상예보 가져오기

        weather_forecast_1st = forecast()
        weather_forecast_data_1st = weather_forecast_1st.get_forecast(today, rows, base_time_1st, nx, ny)
        weather_forecast_data_1st_df = weather_forecast_1st.make_forecast_df(weather_forecast_data_1st)
        weather_forecast_data_1st_df['rainfall'].fillna(method = 'bfill', inplace = True)
        weather_forecast_data_1st_df['snowfall'].fillna(method = 'bfill', inplace = True)
        weather_forecast_tomorrow_1st = weather_forecast_data_1st_df[weather_forecast_data_1st_df.forecast_date == tomorrow] # 내일 데이터 추출
        weather_forecast_tomorrow_1st = pd.DataFrame(weather_forecast_tomorrow_1st)
        weather_forecast_tomorrow_1st['date'] = weather_forecast_tomorrow_1st['forecast_date'] + weather_forecast_tomorrow_1st['forecast_time']
        weather_forecast_tomorrow_1st = weather_forecast_tomorrow_1st.apply(pd.to_numeric)

        # -1차 예측 데이터 만들기

        predict_data_1st = pd.merge(solar_altitude, weather_forecast_tomorrow_1st, how = 'left', on = ['date'])
        predict_data_1st = predict_data_1st.drop(['date', 'announce_date', 'announce_time', 'forecast_date', 'forecast_time'], axis = 1)
        predict_data_1st['temperature'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_1st['rainfall'].fillna(method = 'bfill', inplace = True)
        predict_data_1st['rainfall'].fillna(0, inplace = True)
        predict_data_1st['windvelocity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_1st['humidity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_1st['snowfall'].fillna(method = 'bfill', inplace = True)
        predict_data_1st['snowfall'].fillna(0, inplace = True)
        predict_data_1st['sky'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        # predict_data_1st = predict_data_1st.values

        # -1차 예측 모델 실행

        predict_data_1st_st = sc.transform(predict_data_1st)
        predict_result_tomorrow_1st = model.predict(predict_data_1st_st)
    
        # -1차 예측 결과 정리

        predict_result_tomorrow_1st = pd.DataFrame(predict_result_tomorrow_1st)
        predict_result_tomorrow_1st = pd.concat([predict_data_1st, predict_result_tomorrow_1st], axis = 1)
        predict_result_tomorrow_1st = predict_result_tomorrow_1st[predict_result_tomorrow_1st.altitude > 0]
        predict_result_tomorrow_1st = pd.concat([predict_data_1st, predict_result_tomorrow_1st], axis = 1)
        predict_result_tomorrow_1st.columns = ['hour', 'altitude', 'altitude_change', 'azimuth', 'temperature', 'rainfall', 'windvelocity', 'humidity', 'snowfall', 'sky', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'output']
        predict_result_tomorrow_1st = predict_result_tomorrow_1st.drop(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], axis = 1)
        predict_result_tomorrow_1st['output'].fillna(0, inplace = True)

        # -1차 예측 그래프

        plt.plot(graph_hours, predict_result_tomorrow_1st['output'])
        plt.xlabel('time')
        plt.ylabel('output (kWh)')
        plt.xticks(graph_hours)
        plt.title('1st Predict Result (%s)'% tomorrow)
        print('1차 예측 결과')
        plt.savefig('predict/graph/%s/%s_predict_1st(%s).png'% (name, name, tomorrow), bbox_inches = 'tight', figsize = (10,5), dpi = 300)
        plt.show()
        print('=============================================')

        # -1차 예측 결과 파일로 내보내기

        predict_result_tomorrow_1st.to_csv('predict/data/%s/%s_predict_1st(%s).csv'% (name, name, tomorrow))

    ## 2차 예측 시행

    if hour_today * 100 < int(base_time_2nd):
        pass
    else:

        # -2차 기상예보 가져오기

        weather_forecast_2nd = forecast()
        weather_forecast_data_2nd = weather_forecast_2nd.get_forecast(today, rows, base_time_2nd, nx, ny)
        weather_forecast_data_2nd_df = weather_forecast_1st.make_forecast_df(weather_forecast_data_2nd)
        weather_forecast_data_2nd_df['rainfall'].fillna(method = 'bfill', inplace = True)
        weather_forecast_data_2nd_df['snowfall'].fillna(method = 'bfill', inplace = True)
        weather_forecast_tomorrow_2nd = weather_forecast_data_2nd_df[weather_forecast_data_2nd_df.forecast_date == tomorrow] # 내일 데이터 추출
        weather_forecast_tomorrow_2nd = pd.DataFrame(weather_forecast_tomorrow_2nd)
        weather_forecast_tomorrow_2nd['date'] = weather_forecast_tomorrow_2nd['forecast_date'] + weather_forecast_tomorrow_2nd['forecast_time']
        weather_forecast_tomorrow_2nd = weather_forecast_tomorrow_2nd.apply(pd.to_numeric)

        # -2차 예측 데이터 만들기

        predict_data_2nd = pd.merge(solar_altitude, weather_forecast_tomorrow_2nd, how = 'left', on = ['date'])
        predict_data_2nd = predict_data_2nd.drop(['date', 'announce_date', 'announce_time', 'forecast_date', 'forecast_time'], axis = 1)
        predict_data_2nd['temperature'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_2nd['rainfall'].fillna(method = 'bfill', inplace = True)
        predict_data_2nd['rainfall'].fillna(0, inplace = True)
        predict_data_2nd['windvelocity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_2nd['humidity'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        predict_data_2nd['snowfall'].fillna(method = 'bfill', inplace = True)
        predict_data_2nd['snowfall'].fillna(0, inplace = True)
        predict_data_2nd['sky'].interpolate(method = 'linear', limit_direction = 'forward', inplace = True)
        # predict_data_2nd = predict_data_2nd.values

        # -2차 예측 모델 실행

        predict_data_2nd_st = sc.transform(predict_data_2nd)        
        predict_result_tomorrow_2nd = model.predict(predict_data_2nd_st)

        # -2차 예측 결과 정리

        predict_result_tomorrow_2nd = pd.DataFrame(predict_result_tomorrow_2nd)
        predict_result_tomorrow_2nd = pd.concat([predict_data_2nd, predict_result_tomorrow_2nd], axis = 1)
        predict_result_tomorrow_2nd = predict_result_tomorrow_2nd[predict_result_tomorrow_2nd.altitude > 0]
        predict_result_tomorrow_2nd = pd.concat([predict_data_2nd, predict_result_tomorrow_2nd], axis = 1)
        predict_result_tomorrow_2nd.columns = ['hour', 'altitude', 'altitude_change', 'azimuth', 'temperature', 'rainfall', 'windvelocity', 'humidity', 'snowfall', 'sky', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'output']
        predict_result_tomorrow_2nd = predict_result_tomorrow_2nd.drop(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], axis = 1)
        predict_result_tomorrow_2nd['output'].fillna(0, inplace = True)

        # -2차 예측 그래프

        plt.plot(graph_hours, predict_result_tomorrow_2nd['output'])
        plt.xlabel('time')
        plt.ylabel('output (kWh)')
        plt.xticks(graph_hours)
        plt.title('2nd Predict Result (%s)'% tomorrow)
        print('2차 예측 결과')
        plt.savefig('predict/graph/%s/%s_predict_2nd(%s).png'% (name, name, tomorrow), bbox_inches = 'tight', figsize = (10,5), dpi = 300)
        plt.show()

        # -2차 예측 결과 파일로 내보내기

        predict_result_tomorrow_1st.to_csv('predict/data/%s/%s_predict_2nd(%s).csv'% (name, name, tomorrow))

## 사이트 합계 구하는 함수 실행

if sum_choice == 'Y':
    stage = ['1st', '2nd']
    for i in stage:
        result = site_sum(i)
else:
    pass