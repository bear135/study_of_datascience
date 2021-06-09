# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 09:10:36 2021

@author: myounggyu.kim
"""

import pandas as pd

filename='C:/DB/US_REL_PSN_202011'

psn=pd.read_csv(filename+'.txt',sep='\¶',encoding='UTF-8',header=0)

# 1,221,604 rows

#발명자 제외
#m_psn=pd.DataFrame([])
psn=psn[psn['구분']=='출원인'].reset_index(drop=True).drop(columns=['주소','국적','일련번호'])
# 387,955 rows (Data size 1/3로 감소)

#출원인 이름 전처리 ("주식회사" 와 같이 통상 회사명에 사용되는 단어들 삭제)
garbage_company_name=['PUBLIC','LIMITED','COMPANY','CORP','INC', 'INCORPORATED', 'INCORPORATION', 'GMBH', \
                      'LTD','PLC','CO','INDUSTRIES','IND', 'INDUSTRY', 'KABUSHIKIKAISHA','KK','ENG','ENGINEERING',\
                      'MACH', 'AS', 'AG', 'OY', 'CORPORATION','K.K.','KABUSIKIKAISHA', 'LLC', 'KABUSHIKI', 'KAISHA', \
                      'KABUSIKI']


applicants_list = psn['이름']

new_applicants_list=[]

app_cat=[]


i=0

while i < len(applicants_list):
    
    new_applicant = applicants_list[i].upper()
    
    std_applicant =[]
    
    new_applicant1 = new_applicant.strip().split()
    
    k = 0
    
    for split_applicant in new_applicant1:
    
        split_applicant=split_applicant.replace(',','')
        split_applicant=split_applicant.replace('.','')
        split_applicant=split_applicant.strip()
                        
                      
        for garbage in garbage_company_name:
                            
            if split_applicant == garbage:
                split_applicant = split_applicant.replace(garbage,'')
                split_applicant = split_applicant.strip()
                k = k + 1 
                       
        
        std_applicant.append(split_applicant)
                
    normalized_applicant =" ".join(std_applicant)
    
    new_applicants_list.append(normalized_applicant.strip())   
    
    if k==0:
        app_cat.append('개인')
    else:
        app_cat.append('법인')
    
    i = i + 1
    
psn['변경 출원인']=new_applicants_list

psn['개인/법인']=app_cat

# 법인만 발췌 (개인의 시장참여는 I don't care)

psn1=psn[psn['개인/법인']=='법인']

# 법인만 발췌한 data를 저장

psn1.to_csv(filename+'_M'+'.txt',sep='\t', index=False)
