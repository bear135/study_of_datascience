######################################
## FCP Python 2nd Education code 
######################################

## 기본 패키지 로딩 
import numpy as np 
import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt 
import seaborn as sns 
sns.set(style='whitegrid')

import warnings
warnings.filterwarnings("ignore")

## 한글사용을 설정 
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (15,4)
mpl.rcParams['axes.unicode_minus'] = False

## 데이터 읽어들이기 
df = pd.read_csv('D:/FCP_edu2/data/4) 9월 개질기 운전 밴더_sample.csv', encoding = 'cp949')
print(df.shape)
df.head()

'''
#파일이 여러개일 경우는 아래와 같이 할 수 도 있다. 
df_09 = pd.read_csv('data/4) 9월 개질기 운전 밴더_sample.csv', encoding = 'cp949')
df_10 = pd.read_csv('data/4) 10월 개질기 운전 밴더_sample.csv', encoding = 'cp949')
df_11 = pd.read_csv('data/4) 11월 개질기 운전 밴더_sample.csv', encoding = 'cp949')
df = pd.concat(df_09, df_10,df_11)

엑셀파일을 불러오려면 
import xlrd
df = pd.read_excel('경로/파일명', sheet_name = '시트명')
'''

## 장비시간 컬럼을 H:M:S 포맷으로 바꿔줘야 한다. 
import datetime 

for i in range(df['장비시간'].count()):
    df['장비시간'][i] = str(datetime.timedelta(df['장비시간'][i])) 
    
df['장비시간'].head(10)

## 장비날짜와 장비시간을 합쳐서 새로운 컬럼 equit_dt를 만들자 
df['equip_dt'] = df['장비날짜'] + ' ' + df['장비시간']
df['equip_dt'] = pd.to_datetime(df['equip_dt'])
df['equip_dt'].head()

### 1. 분석대상 변수를 지정한다. (리스트 직접 입력 방식)
var_list_1 = ['ACP', 'TT102', 'TT120', 'TT109', 'TT112']
var_list_1

### 5개 센서들의 통계량 한꺼번에 구하기 
print( df[var_list_1].mean() )
print( df[var_list_1].min() )
print( df[var_list_1].max() )

df[var_list_1].describe()

## 2. 분석 대상 변수를 파일로 부터 불러오기. 
var_list_2 = pd.read_csv('data/charting_list.csv')
var_list_2 = var_list_2['var']
var_list_2

## 21개 변수들의 통계량 구하기 
df[var_list_2].describe()

## 통계량을 csv 파일로 내보내기 
df_stat = pd.DataFrame(df[var_list_2].describe())
df_stat.to_csv('output/stat_Sep_2020.csv')

## 3. 그래프 한꺼번에 그리기 - matplotlib 

for i in var_list_2 : 
    plt.figure(figsize = (20,4))   ## 차트의 사이즈 지정 (옵션)
    plt.title('%s' %i)             ## 차트의 타이틀 지정 (옵션)
    df[i].plot()
    plt.savefig('img/%s.png' %i)   ## 차트를 이미지파일로 저장 (옵션)   
    
## 4. 그래프 한꺼번에 그리기 - seaborn

for i in var_list_2 : 
    plt.figure(figsize = (18,3))   ## 차트의 사이즈 지정 (옵션)
    plt.title('%s' %i)             ## 차트의 타이틀 지정 (옵션)
    sns.lineplot(data = df, x = 'day', y= i, ci = 0)
    plt.savefig('img/%s.png' %i)   ## 차트를 이미지파일로 저장 (옵션)