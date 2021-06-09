# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 21:46:00 2021

@author: kmang
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches



########################################## 1st filter ############################################
yearly_patents = pd.read_csv('C:/DB/AWS/AWS_yearly patents per ipc.csv',index_col=0)

yearly_applicants = pd.read_csv('C:/DB/AWS/AWS_yearly applicants per ipc.csv',index_col=0)


sorted_yearly_patents = yearly_patents.sum(axis=1).sort_values(ascending=False)

#yearly_patents = yearly_patents.fillna(1)
#yearly_applicants = yearly_applicants.fillna(1)


# Accumulated patents ranking No. 1 ~ 10, period is 10 years

ranking = 300

sorted_ipc = list (sorted_yearly_patents.index)[0:ranking]

#top_ipc = sorted_ipc[0]
#bottom_ipc = sorted_ipc[-1]

year = list(yearly_patents.columns)

# display_ipc = display_ipc[0:ranking]

#year = list(range(start_year,end_year+1))


###  IPC such as G06F 17/60 was changed into G06Q .... after 2006
###  so, G06Q should be changed G06F 17/60 after 2006




#  Graph
period = int(year[-1])-int(year[0])+1

averaged_patents = sorted_yearly_patents.iloc[0:ranking].sum() / len(sorted_ipc) / period


displayed_applicants=pd.DataFrame([],columns=yearly_applicants.columns)

displayed_patents=pd.DataFrame([],columns=yearly_applicants.columns)

for ipc in sorted_ipc:
    
    displayed_applicants.loc[ipc,:]=yearly_applicants.loc[ipc]
    
    displayed_patents.loc[ipc,:]=yearly_patents.loc[ipc]

# x: applicants,  y: patents    
global_x_max = int(displayed_applicants.max().max())
global_x_min = int(displayed_applicants.min().min())

global_y_max = int(displayed_patents.max().max())
global_y_min = int(displayed_patents.min().min())

sorted_displayed_applicants = displayed_applicants.sum(axis=1).sort_values(ascending=False)

averaged_applicants = sorted_displayed_applicants.iloc[0:ranking].sum() / len(sorted_ipc) / period

 
ipc = list(displayed_applicants.index)


# technology growth trend analysis using applicants and patents

# plot 2x2 matrix    
# x: applicants  y: patents 


x_mean = round(averaged_applicants,1)

y_mean = round(averaged_patents,1)


x_top_max = int(displayed_applicants.max().max())
y_top_max = int(displayed_patents.max().max())

x_min = int(displayed_applicants.min().min())
y_min = int(displayed_patents.min().min())


ipc_statistics = ['accumulated patents', 'accumulated applicants', 'averaged patents', \
                    'averaged applicants', 'averaged weighted CAGR of patents', \
                    'averaged weighted CAGR of applicants']

ipc_analysis_data=pd.DataFrame([],index=sorted_ipc, columns=ipc_statistics)

ipc_analysis_data['accumulated patents']=list(displayed_patents.sum(axis=1))
ipc_analysis_data['accumulated applicants']=list(displayed_applicants.sum(axis=1))
ipc_analysis_data['averaged patents']=list(displayed_patents.mean(axis=1))
ipc_analysis_data['averaged applicants']=list(displayed_applicants.mean(axis=1))


weight = list(range(1, len(year)))


def CAGR (initial, final, period):
    
    cagr = pow((final/initial),(1/period)) - 1   
     
    return round(cagr,3)

i = 0

while i < len(ipc):
    
    ipc_patents = list(displayed_patents.loc[ipc[i]])
    ipc_applicants = list(displayed_applicants.loc[ipc[i]])
    
    j = 1
    
    weight_accum_cagr1 = 0
    weight_accum_cagr2 = 0
    
    while j < len (ipc_patents):
        
        
        if ipc_patents[0]==0: ipc_patents[0]=1 
       
        if ipc_applicants[0]==0: ipc_applicants[0]=1
        
        cagr1 = CAGR(ipc_patents[0], ipc_patents[j], j)
        cagr2 = CAGR(ipc_applicants[0], ipc_applicants[j], j)
     
        weight_accum_cagr1 = weight[j-1]*cagr1 + weight_accum_cagr1
        weight_accum_cagr2 = weight[j-1]*cagr2 + weight_accum_cagr2

        
#        if ipc_patents[0] !=0: 
        
#            cagr1 = CAGR(ipc_patents[0], ipc_patents[j], j)
#            cagr2 = CAGR(ipc_applicants[0], ipc_applicants[j], j)
     
#            weight_accum_cagr1 = weight[j-1]*cagr1 + weight_accum_cagr1
#            weight_accum_cagr2 = weight[j-1]*cagr2 + weight_accum_cagr2

#        elif ipc_patents[1] !=0:
            
#            cagr1 = CAGR(ipc_patents[0], ipc_patents[j], j)
            
            
#        if ipc_applicants[0] != 0:
            
#            cagr1 = CAGR(ipc_patents[0], ipc_patents[j], j)
#            cagr2 = CAGR(ipc_applicants[0], ipc_applicants[j], j)
 
#            weight_accum_cagr1 = weight[j-1]*cagr1 + weight_accum_cagr1
#            weight_accum_cagr2 = weight[j-1]*cagr2 + weight_accum_cagr2

        j = j + 1
        
    weight_accum_cagr1 = weight_accum_cagr1/sum(weight)
    
    weight_accum_cagr2 = weight_accum_cagr2/sum(weight)
    
    ipc_analysis_data.loc[ipc[i],'averaged weighted CAGR of patents'] = round(weight_accum_cagr1,3)
    
    ipc_analysis_data.loc[ipc[i],'averaged weighted CAGR of applicants'] = round(weight_accum_cagr2,3)
    
    i = i + 1


saved_file_name='C:\DB\AWS\TOP' + " "+ str(ranking) + " " + "ipc analysis.csv"

ipc_analysis_data.to_csv(saved_file_name)

# ipc picking
# plot 2x2 matrix    
# x: applicants  y: patents 

x_plus_range = x_mean + (x_top_max - x_mean)*0.6
x_minus_range = x_mean - (x_top_max - x_mean)*0.05


y_plus_range = y_mean + (y_top_max - y_mean)*0.6
y_minus_range = y_mean - (y_top_max - y_mean)*0.05

patent_cagr = 0.05
applicant_cagr = 0.05


# plot 2x2 matrix    
# x: applicants  y: patents 

mask1 = (ipc_analysis_data['averaged applicants'] >= x_minus_range) & (ipc_analysis_data['averaged applicants'] <= x_plus_range)

mask2 = (ipc_analysis_data['averaged patents'] >= y_minus_range) & (ipc_analysis_data['averaged patents'] <= y_plus_range) 

mask3 = ipc_analysis_data['averaged weighted CAGR of patents'] > patent_cagr

mask4 = ipc_analysis_data['averaged weighted CAGR of applicants'] > applicant_cagr

#print("The max, min and average values of patents of the picked %d IPC are %d, %d, %d" %(ranking, y_top_max, y_min, y_mean ))
print("The average patents # of the picked IPC is from %d to %d" % (round(y_minus_range,1), round(y_plus_range,1)))

#print("The max, min and average values of applicants of the picked %d IPC are %d, %d, %d" %(ranking, x_top_max, x_min, x_mean ))
print("The average applicants # of the picked IPC is from %d to %d" % (round(x_minus_range,1), round(x_plus_range,1)))
print("The averaged weighted CAGR of patents of the picked IPC is from %d %%" % (patent_cagr*100))
print("The averaged weighted CAGR of applicants of the picked IPC is from %d %%" % (applicant_cagr*100))



ipc_set1 = set(list(ipc_analysis_data.loc[mask1].index))
ipc_set2 = set(list(ipc_analysis_data.loc[mask2].index))
ipc_set3 = set(list(ipc_analysis_data.loc[mask3].index))
ipc_set4 = set(list(ipc_analysis_data.loc[mask3].index))

temp_picked_ipc1 = ipc_set1.intersection(ipc_set2)
temp_picked_ipc2 = ipc_set3.intersection(ipc_set4)

Fst_picked_ipc = temp_picked_ipc1.intersection(temp_picked_ipc2)

print("The 1st picked IPC no. is %d" % len(Fst_picked_ipc))

# IPC dynamics of the picked_ipc

Fst_picked_ipc_applicants=pd.DataFrame([],columns=yearly_applicants.columns)

Fst_picked_ipc_patents=pd.DataFrame([],columns=yearly_applicants.columns)

for ipc in Fst_picked_ipc:
    
    Fst_picked_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]


sorted_picked_ipc_patents = Fst_picked_ipc_patents.sum(axis=1).sort_values(ascending=False)

sorted_Fst_picked_ipc = list(sorted_picked_ipc_patents.index)

for ipc in sorted_Fst_picked_ipc:
    
    Fst_picked_ipc_applicants.loc[ipc,:]=yearly_applicants.loc[ipc]
    
    Fst_picked_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]

 
############################################ 2nd filter #################################################

# input raw data information
filename1='C:/DB/AWS/AWS_ipc300_confusion_matrix.csv'

pat_data = pd.read_csv(filename1,encoding='UTF-8', index_col=0)

IPC_x = list(pat_data.columns)
IPC_y = list(pat_data.index)

ipc_confusion_list = []

# ipc의 section, class, sub-class 수준에서 달라야 서로 다른 기술분야로 볼 수 있음
# main group 및 sub group이 다른 경우에는 동일 기술분야로 봐야..
# e.g. A01B 와 A01C는 서로 다른 기술분야로 볼 수 있지만, A01B 01/002와 A01B 02/02는 서로 동일 기술분야로 간주함

i = 0

for ipcy in IPC_y :
    
    j = 0
    
    ipc_confusion_index = 0
    
    for ipcx in IPC_x :
        
        if ipcx[0:4] != ipcy[0:4]:
            
           ipc_confusion_index = ipc_confusion_index + pat_data.loc[ipcy,ipcx]
    
    ipc_confusion_list.append(ipc_confusion_index)


pat_data['IPC confusion'] = ipc_confusion_list

#pat_data.to_csv('C:/DB/AWS/AWS_ipc300_confusion_index.csv')


pat_data=pat_data.sort_values('IPC confusion', ascending=False)

rank1 = 100

candidateIPC = set(list(pat_data.index)[0:rank1])

Snd_picked_ipc = Fst_picked_ipc.intersection(candidateIPC)

print("The 2nd Picked IPC no. is %d" % len(Snd_picked_ipc))


########################################## 3rd filter ############################################

filename3 = 'C:/DB/AWS/2001_2010_US_assignment_IPC.csv'

us_assignment_ipc_data = pd.read_csv(filename3)

sorted_us_assignment_ipc = us_assignment_ipc_data['IPC'].value_counts()

top_rank = 100

us_assignment_ipc = list(sorted_us_assignment_ipc.index)[0:top_rank]

candidateIPC1 = set(us_assignment_ipc)


#### Finally (3rd) Picked IPC : Trd_picked_ipc

Trd_picked_ipc = Snd_picked_ipc.intersection(candidateIPC1)

Trd_picked_ipc_applicants=pd.DataFrame([],columns=yearly_applicants.columns)

Trd_picked_ipc_patents=pd.DataFrame([],columns=yearly_applicants.columns)

for ipc in Trd_picked_ipc:
    
    Trd_picked_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]


sorted_Trd_picked_ipc_applicants = Trd_picked_ipc_patents.sum(axis=1).sort_values(ascending=False)

sorted_Trd_picked_ipc = list(sorted_Trd_picked_ipc_applicants.index)

for ipc in sorted_Trd_picked_ipc:
    
    Trd_picked_ipc_applicants.loc[ipc,:]=yearly_applicants.loc[ipc]
    
    Trd_picked_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]
    
print("The 3rd(finally) Picked IPC no. is %d" % len(sorted_Trd_picked_ipc))

########################################## IPC & Technology matching ############################################

filename4 = 'C:/DB/AWS/IPC_Tech_matching1.csv'

IPC_Tech_correlation_data = pd.read_csv(filename4, encoding='UTF-8')

i = 0

tech_ipc_list = []
    
while i < 10:
    
    ipc = 'IPC' + str(i+1)
    
    ipc_list = list(IPC_Tech_correlation_data[ipc])
    
   
    for ipca in ipc_list:
        
        if ipca != '-1':
                     
            tech_ipc_list.append(ipca)
    
    i = i + 1
         
IPC_Tech_correlation_data1 = pd.DataFrame([])

IPC_Tech_correlation_data1["IPC"]=tech_ipc_list

IPC_Tech_correlation_data1 = IPC_Tech_correlation_data1["IPC"].value_counts()

IPC_Tech_correlation_set = set(tech_ipc_list)


###### Matched ones out of Finally(3rd) picked IPC(s) : Tech_matched_ipc


Tech_matched_ipc = Trd_picked_ipc.intersection(IPC_Tech_correlation_set)

print("The matched IPC no. with the promising Tech. out of the finally selected IPC(s) is %d" % len(Tech_matched_ipc))

Fst_3rd_common_ipc = set(ipc_analysis_data.index).intersection(IPC_Tech_correlation_set)

j = 0

matching_no = []

matching_ipc = []

while j < len(IPC_Tech_correlation_data.index):
    
    IPC_tech_set=list(IPC_Tech_correlation_data.iloc[j,3:13])
    
    temp_matching_ipc = Tech_matched_ipc.intersection(IPC_tech_set)
    
    matching_ipc.append(list(temp_matching_ipc))
    
    matching_no.append(len(temp_matching_ipc))
    
    j = j + 1
    
    
IPC_Tech_correlation_data['Matching IPC with the finally selected IPC(s)'] = matching_ipc
IPC_Tech_correlation_data['Matching IPC(s) no.'] = matching_no


############################## Tehc matched IPC ouf of the finally (3rd) picked IPC(s) Graph ####################

Tech_matched_ipc_applicants=pd.DataFrame([],columns=yearly_applicants.columns)

Tech_matched_ipc_patents=pd.DataFrame([],columns=yearly_applicants.columns)

for ipc in Tech_matched_ipc:
    
    Tech_matched_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]


sorted_Tech_matched_ipc_patents = Tech_matched_ipc_patents.sum(axis=1).sort_values(ascending=False)

sorted_Tech_matched_ipc = list(sorted_Tech_matched_ipc_patents.index)

for ipc in sorted_Tech_matched_ipc:
    
    Tech_matched_ipc_applicants.loc[ipc,:]=yearly_applicants.loc[ipc]
    
    Tech_matched_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]



y_point1 = [0]
x_point2 = [0]
    
i = 1
    
while i <  len(sorted_Tech_matched_ipc_patents.index):
        
    y_value=int(global_y_max / (len(sorted_Tech_matched_ipc_patents.index)-i) )
        
    y_point1.append(y_value)
        
    x_value=int(global_x_max / (len(sorted_Tech_matched_ipc_patents.index)-i) )
        
    x_point2.append(x_value)
        
    i = i + 1
    
    

x_point1 = [x_mean]
y_point2 = [y_mean]
    
i = 1
    
while i < len(y_point1):
    
    x_point1.append(x_mean)
    
    y_point2.append(y_mean)
    
    i = i + 1   
    
    
j = 0 

ylabel_max = 0

num_per_graph = 5

#graph_no1 = int(len(sorted_Tech_matched_ipc) / num_per_graph)
#graph_no2 = (len(sorted_Tech_matched_ipc)) % num_per_graph


#top_ipc = sorted_ipc[0]
#bottom_ipc = sorted_ipc[-1]

while j < len(sorted_Tech_matched_ipc)  :
    
    
    if len(sorted_Tech_matched_ipc) - j >= num_per_graph:
    
        fig_title = 'Tech matched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + num_per_graph) + "  " + 'DYNAMICS'
        

#       x, y axis ranges are changed with the corresponding values of the selected IPC
#       x_max = int(Trd_picked_ipc_applicants.iloc[j:j+5].max().max())
#       y_max = int(Trd_picked_ipc_patents.iloc[j:j+5].max().max())
    

#  x, y axis are fixed with the max / min 

# top_ipc = sorted_ipc[0]
# bottom_ipc = sorted_ipc[-1]

   
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+1]]
        y2 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_matched_ipc[j+1])
    
    
        x3 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+2]]
        y3 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_matched_ipc[j+2])
    
        x4 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+3]]
        y4 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+3]]
        plt.scatter(x4, y4, marker="o", label=sorted_Tech_matched_ipc[j+3])
    
        x5 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+4]]
        y5 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+4]]
        plt.scatter(x5, y5, marker="D", label=sorted_Tech_matched_ipc[j+4])
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    

    
    
        year_trend1 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
        year_trend4 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+3],:])
        year_trend4 = year_trend4[0:10]

        if max(year_trend4) > ylabel_max: ylabel_max = max(year_trend4)
        
        year_trend5 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+4],:])
        year_trend5 = year_trend5[0:10]
    
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_matched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_matched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_matched_ipc[j+2])
        plt.plot(time_axis,year_trend4,color='yellow',label=sorted_Tech_matched_ipc[j+3])
        plt.plot(time_axis,year_trend5,color='green',label=sorted_Tech_matched_ipc[j+4])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()
    
    elif  len(sorted_Tech_matched_ipc) - j == 1:
        
               
        fig_title = 'Tech matched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + "  " + 'DYNAMICS'
        
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    
    
        year_trend1 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    
        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
           
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_matched_ipc[j])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()
    
    elif  len(sorted_Tech_matched_ipc) - j == 2:

        fig_title = 'Tech matched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 2) + "  " + 'DYNAMICS'
     

 
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+1]]
        y2 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_matched_ipc[j+1])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
   
    
        year_trend1 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
 
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_matched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_matched_ipc[j+1])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()    
    
    elif  len(sorted_Tech_matched_ipc) - j == 3:
        
        fig_title = 'Tech matched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 3) + "  " + 'DYNAMICS'
    
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+1]]
        y2 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_matched_ipc[j+1])
    
    
        x3 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+2]]
        y3 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_matched_ipc[j+2])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    

    
    
        year_trend1 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
   
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_matched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_matched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_matched_ipc[j+2])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()    
    
    elif  len(sorted_Tech_matched_ipc) - j == 4:
        
        fig_title = 'Tech matched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 4) + "  " + 'DYNAMICS'
    
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+1]]
        y2 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_matched_ipc[j+1])
    
    
        x3 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+2]]
        y3 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_matched_ipc[j+2])
    
        x4 = Tech_matched_ipc_applicants.loc[sorted_Tech_matched_ipc[j+3]]
        y4 = Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+3]]
        plt.scatter(x4, y4, marker="o", label=sorted_Tech_matched_ipc[j+3])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
   
    
        year_trend1 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
        year_trend4 = list(Tech_matched_ipc_patents.loc[sorted_Tech_matched_ipc[j+3],:])
        year_trend4 = year_trend4[0:10]

        if max(year_trend4) > ylabel_max: ylabel_max = max(year_trend4)
        
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_matched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_matched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_matched_ipc[j+2])
        plt.plot(time_axis,year_trend4,color='yellow',label=sorted_Tech_matched_ipc[j+3])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()   
  
    
    j = j + num_per_graph
    
    
    
############################## Tehc unmatched IPC ouf of the finally (3rd) picked IPC(s) Graph ####################

Tech_unmatched_ipc = Trd_picked_ipc.difference(IPC_Tech_correlation_set)

Tech_unmatched_ipc_applicants=pd.DataFrame([],columns=yearly_applicants.columns)

Tech_unmatched_ipc_patents=pd.DataFrame([],columns=yearly_applicants.columns)

for ipc in Tech_unmatched_ipc:
    
    Tech_unmatched_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]


sorted_Tech_unmatched_ipc_patents = Tech_unmatched_ipc_patents.sum(axis=1).sort_values(ascending=False)

sorted_Tech_unmatched_ipc = list(sorted_Tech_unmatched_ipc_patents.index)

for ipc in sorted_Tech_unmatched_ipc:
    
    Tech_unmatched_ipc_applicants.loc[ipc,:]=yearly_applicants.loc[ipc]
    
    Tech_unmatched_ipc_patents.loc[ipc,:]=yearly_patents.loc[ipc]



y_point1 = [0]
x_point2 = [0]
    
i = 1
    
while i <  len(sorted_Tech_unmatched_ipc_patents.index):
        
    y_value=int(global_y_max / (len(sorted_Tech_unmatched_ipc_patents.index)-i) )
        
    y_point1.append(y_value)
        
    x_value=int(global_x_max / (len(sorted_Tech_unmatched_ipc_patents.index)-i) )
        
    x_point2.append(x_value)
        
    i = i + 1
    
    

x_point1 = [x_mean]
y_point2 = [y_mean]
    
i = 1
    
while i < len(y_point1):
    
    x_point1.append(x_mean)
    
    y_point2.append(y_mean)
    
    i = i + 1   
    
    
j = 0 

ylabel_max = 0

num_per_graph = 5

#graph_no1 = int(len(sorted_Tech_matched_ipc) / num_per_graph)
#graph_no2 = (len(sorted_Tech_matched_ipc)) % num_per_graph


#top_ipc = sorted_ipc[0]
#bottom_ipc = sorted_ipc[-1]

while j < len(sorted_Tech_unmatched_ipc)  :
    
    
    if len(sorted_Tech_unmatched_ipc) - j >= num_per_graph:
    
        fig_title = 'Tech unmatched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + num_per_graph) + "  " + 'DYNAMICS'
        

#       x, y axis ranges are changed with the corresponding values of the selected IPC
#       x_max = int(Trd_picked_ipc_applicants.iloc[j:j+5].max().max())
#       y_max = int(Trd_picked_ipc_patents.iloc[j:j+5].max().max())
    

#  x, y axis are fixed with the max / min 

# top_ipc = sorted_ipc[0]
# bottom_ipc = sorted_ipc[-1]

   
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j]]
        y1 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_unmatched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+1]]
        y2 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_unmatched_ipc[j+1])
    
    
        x3 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+2]]
        y3 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_unmatched_ipc[j+2])
    
        x4 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+3]]
        y4 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+3]]
        plt.scatter(x4, y4, marker="o", label=sorted_Tech_unmatched_ipc[j+3])
    
        x5 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+4]]
        y5 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+4]]
        plt.scatter(x5, y5, marker="D", label=sorted_Tech_unmatched_ipc[j+4])
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    

    
    
        year_trend1 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
        year_trend4 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+3],:])
        year_trend4 = year_trend4[0:10]

        if max(year_trend4) > ylabel_max: ylabel_max = max(year_trend4)
        
        year_trend5 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+4],:])
        year_trend5 = year_trend5[0:10]
    
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_unmatched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_unmatched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_unmatched_ipc[j+2])
        plt.plot(time_axis,year_trend4,color='yellow',label=sorted_Tech_unmatched_ipc[j+3])
        plt.plot(time_axis,year_trend5,color='green',label=sorted_Tech_unmatched_ipc[j+4])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()
    
    elif  len(sorted_Tech_unmatched_ipc) - j == 1:
        
               
        fig_title = 'Tech Unmatched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + "  " + 'DYNAMICS'
        
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j]]
        y1 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_unmatched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    
    
        year_trend1 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    
        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
           
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_unmatched_ipc[j])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()
    
    elif  len(sorted_Tech_unmatched_ipc) - j == 2:

        fig_title = 'Tech Unmatched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 2) + "  " + 'DYNAMICS'
     

 
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_matched_ipc[j]]
        y1 = Tech_unmatched_ipc_patents.loc[sorted_Tech_matched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_matched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+1]]
        y2 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_unmatched_ipc[j+1])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
   
    
        year_trend1 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
 
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_unmatched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_unmatched_ipc[j+1])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()    
    
    elif  len(sorted_Tech_unmatched_ipc) - j == 3:
        
        fig_title = 'Tech Unmatched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 3) + "  " + 'DYNAMICS'
    
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j]]
        y1 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_unmatched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+1]]
        y2 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_unmatched_ipc[j+1])
    
    
        x3 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+2]]
        y3 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_unmatched_ipc[j+2])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
    

    
    
        year_trend1 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
   
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_unmatched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_unmatched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_unmatched_ipc[j+2])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()    
    
    elif  len(sorted_Tech_unmatched_ipc) - j == 4:
        
        fig_title = 'Tech Unmatched IPC out of Final IPC(s).' + 'No. ' + str(j + 1) + ' ~ ' + str(j + 4) + "  " + 'DYNAMICS'
    
        plt.figure()
        plt.title(fig_title)
        plt.plot(x_point1,y_point1,linestyle='--')
        plt.plot(x_point2,y_point2,linestyle='--')
        x1 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j]]
        y1 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j]]
        plt.scatter(x1, y1, marker=">", label=sorted_Tech_unmatched_ipc[j])
        plt.axis([0,global_x_max,0,global_y_max])
    
        x2 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+1]]
        y2 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1]]
        plt.scatter(x2, y2, marker=r"h", label=sorted_Tech_unmatched_ipc[j+1])
    
    
        x3 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+2]]
        y3 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2]]
        plt.scatter(x3, y3, marker='s', label=sorted_Tech_unmatched_ipc[j+2])
    
        x4 = Tech_unmatched_ipc_applicants.loc[sorted_Tech_unmatched_ipc[j+3]]
        y4 = Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+3]]
        plt.scatter(x4, y4, marker="o", label=sorted_Tech_unmatched_ipc[j+3])
    
        plt.legend()
        plt.xlabel('Applicants')
        plt.ylabel('Patents')
        plt.show()
    
   
    
        year_trend1 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j],:])
        year_trend1 = year_trend1[0:10]
    

        if max(year_trend1) > ylabel_max: ylabel_max = max(year_trend1)
    
        year_trend2 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+1],:])
        year_trend2 = year_trend2[0:10]
    
        if max(year_trend2) > ylabel_max: ylabel_max = max(year_trend2)
    
        year_trend3 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+2],:])
        year_trend3 = year_trend3[0:10]

        if max(year_trend3) > ylabel_max: ylabel_max = max(year_trend3)
        
        year_trend4 = list(Tech_unmatched_ipc_patents.loc[sorted_Tech_unmatched_ipc[j+3],:])
        year_trend4 = year_trend4[0:10]

        if max(year_trend4) > ylabel_max: ylabel_max = max(year_trend4)
        
        time_axis = year
    
        plt.figure()
        plt.xlabel('year')
        plt.ylabel('patents')
        plt.title(fig_title)
        plt.ylim(0, ylabel_max)
        plt.plot(time_axis,year_trend1,color='black',label=sorted_Tech_unmatched_ipc[j])
        plt.plot(time_axis,year_trend2,color='blue', label=sorted_Tech_unmatched_ipc[j+1])
        plt.plot(time_axis,year_trend3,color='red', label=sorted_Tech_unmatched_ipc[j+2])
        plt.plot(time_axis,year_trend4,color='yellow',label=sorted_Tech_unmatched_ipc[j+3])
        plt.legend(bbox_to_anchor=(0.0,0.95,0.2,0.05),loc='upper left')
        plt.show()   
  
    
    j = j + num_per_graph