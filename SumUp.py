
# -*- coding: utf-8 -*-

"""

Created on Thu Sep  7 11:09:01 2023

 

@author: ZhangW16

"""

 

# -*- coding: utf-8 -*-

"""

Created on Tue Sep  5 17:17:07 2023

 

@author: ZhangW16

"""

import matplotlib.pyplot as plt

import pandas as pd

import numpy as np

import datetime

from datetime import timedelta

import plotly.express as px

# 侧边栏

import streamlit as st

st.sidebar.title('Please Choose Date')

date = st.sidebar.date_input('Start Date', datetime.date(2023, 7, 1))

time = st.sidebar.time_input('Start Time', datetime.time(20,00,0,0))

filter1= datetime.datetime.combine(date, time)

date1 = st.sidebar.date_input('End Date', datetime.date(2023, 7, 18))

time1 = st.sidebar.time_input('Endt Time', datetime.time(20,00,0,0))

filter2= datetime.datetime.combine(date1, time1)

 

 

 

# charttype="by day"

# filter1=datetime.datetime(2023, 7, 1, 20)

# filter2=datetime.datetime(2023, 7, 20, 20)

 

 

st.title('Start Your Fantastic Data Journey')

 

st.header('Cutter Utilization Summary')

 

cycle1=("Cutter 105","Cutter 107","Cutter 108")

chooseM=st.selectbox('Please Select the Cutter Number',cycle1)

 

 

dfbase105=pd.read_excel('Cutter\\datebase105.xlsx')

dfbase107=pd.read_excel('Cutter\\datebase107.xlsx')

dfbase108=pd.read_excel('Cutter\\datebase108.xlsx')

dfbase105['date'] = pd.to_datetime(dfbase105['date'])

indexfirszero=(dfbase105.loc[dfbase105['Week1'] == 0].index.tolist())[0]

 

# filter1=datetime.datetime(2023, 7, 15, 20, 30,00)

# testendtim=datetime.datetime(2023, 7, 20, 8, 30,00)

di=0

if filter2<dfbase105.iloc[indexfirszero-1,0]:

    di=1

else:

    di=0





# filter1=datetime.datetime(2023, 7, 1, 20)

# filter2=datetime.datetime(2023, 7, 18, 20)

# writer = pd.ExcelWriter("C:\\Cutter\\datebase.xlsx")

# dfbase.to_excel(writer, index=False, sheet_name='Sheet1')

# writer.save()

# writer.close()

 

 

# dfbase=pd.read_excel(r'C:\\Cutter\\datebase.xlsx')

# dfbase['date'] = pd.to_datetime(dfbase['date'])

summarybar=[]

labablebar=[]

baseline=[]

baselinedata=0.5

dfbase105 = dfbase105[dfbase105['date'] >= filter1]    

dfbase105 = dfbase105[dfbase105['date'] <= filter2]   

summarybar.append(round(np.mean(dfbase105['Excute']),2))

labablebar.append('Cutter 105')

baseline.append(baselinedata)

 

dfbase107= dfbase107[dfbase107['date'] >= filter1]    

dfbase107= dfbase107[dfbase107['date'] <= filter2]   

summarybar.append(round(np.mean(dfbase107['Excute']),2))

baseline.append(baselinedata)

labablebar.append('Cutter 107')

 

 

dfbase108= dfbase108[dfbase108['date'] >= filter1]    

dfbase108= dfbase108[dfbase108['date'] <= filter2]   

summarybar.append(round(np.mean(dfbase108['Excute']),2))

baseline.append(baselinedata)

labablebar.append('Cutter 108')

 

fig = plt.figure(figsize=(8, 6))

bar1=plt.bar(labablebar, summarybar)

plt.bar_label(bar1)

# 在次坐标轴上绘制折线图

# ls:线的类型，lw：宽度

plt.plot(labablebar, baseline, ls='--', lw=2, color='r',ms = 20, mfc = 'm')


# 设置次坐标轴的取值范围，避免折线图波动过大，这里默认显示

st.pyplot(plt)

st.header('Next Show The Uptime and CT you choosen')

# st.title('Next Show The Uptime and CT you choosen')

cycle=("by week","by day")

charttype=st.selectbox('Please Summary cycle',cycle)

 

if chooseM=="Cutter 105":

    dfbase=dfbase105

    tagname='HFWR.XYC105.EQUIP_STAT'

    tagnameC='HFWR.XYC105.EQUIP_CUTTME'

    tagnamere='HFWR.XYC105.EQUIP_RECIPE'

if chooseM=="Cutter 107":

    dfbase=dfbase107

    tagnameC='HFWR.XYC107.EQUIP_CUTTME'

    tagname='HFWR.XYC107.EQUIP_STAT'

    tagnamere='HFWR.XYC107.EQUIP_RECIPE'

if chooseM=="Cutter 108":

    dfbase=dfbase108

    tagnameC='HFWR.XYC108.EQUIP_CUTTME'

    tagname='HFWR.XYC108.EQUIP_STAT'

    tagnamere='HFWR.XYC108.EQUIP_RECIPE'

 

    

if charttype=="by week":

    colist=[]

    lablelistsu=['Excute','Idle','Stopped','Suspended','Aborted','Starting','Stopping','Aborting','Holding','Held','Unholding','Suspending','Unsuspending','Resetting','Completing','Complete','Clearing','Turnoff','Changover']

    colist.append('Week1')

    colist=colist+lablelistsu

    bar=pd.DataFrame(columns=colist)

    for i in range(dfbase.iloc[0,20],dfbase.iloc[-1,20]+1):

        bar.loc[i-dfbase.iloc[0,20],'Week1']=i

        for j in range(1,len(lablelistsu)+1):

            bar.iloc[i-dfbase.iloc[0,20],j]=np.mean(dfbase[dfbase['Week1']==i][lablelistsu[j-1]])

    colorS=['g','y','r','c','m','SeaGreen','OrangeRed','SteelBlue','LightSkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Aqua','DarkTurquoise','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen']   

    # colorS=['SeaGreen','y','OrangeRed','LightPink','LightSkyBlue','SkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Cyan','Aqua','DarkTurquoise','SeaGreen','y','OrangeRed','SteelBlue','LightSkyBlue','SkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Cyan','Aqua','DarkTurquoise','OrangeRed']

    # colorS=['g','y','r','c','m','SeaGreen','OrangeRed','SteelBlue','LightSkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Aqua','DarkTurquoise']

    bottomS=bar.iloc[:,1]

    fig, ax = plt.subplots(figsize=(8, 6))

    alphaS=[0.5,0.6,0.7]

    bar_plot1=ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,1],label=bar.columns[1],color=colorS[0])

    for rect,i in zip(bar_plot1,range(len(bar.iloc[:,1]))):

        height_1=bar.iloc[i,1]

        ax.text(rect.get_x() + rect.get_width()/2., height_1-0.08, "%.2f" % height_1,

                ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')


    ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,2],bottom=bottomS,label=bar.columns[2],color=colorS[1])


    for rect,ih in zip(bar_plot1,range(len(bar.iloc[:,2]))):

        if bar.iloc[ih,2]>0.1:

            height_1h=bar.iloc[ih,2]+bar.iloc[ih,1]

            ax.text(rect.get_x() + rect.get_width()/2., height_1h-0.08, "%.2f" % bar.iloc[ih,2],

                    ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')

        #bar.shape[1]-1

    for isa in range(3,bar.shape[1]-1):

        if sum(bar.iloc[:,isa])>0:

            for k in range(isa,isa+1):

              bottomS=bottomS+ bar.iloc[:,isa-1]

            ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,isa],bottom=bottomS,label=bar.columns[isa],color=colorS[isa-1])

            for rect,ik in zip(bar_plot1,range(len(bar.iloc[:,isa]))):

                if bar.iloc[ik,isa]>0.1:

                    height_1k=0

                    for su in range(1,isa+1):

                        height_1k=height_1k+bar.iloc[ik,su]

                    ax.text(rect.get_x() + rect.get_width()/2., height_1k-0.05, "%.2f" % bar.iloc[ik,isa],

                            ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')

    #     # ax.bar(df['Time'].astype(str), df['LiAuto'],label='LiAuto',color=['r','w','w'],alpha=0.8)

    # # ax.bar(df['Time'].astype(str), df['BMW'], bottom=df['LiAuto'], label='BMW',color=['w','g','w'],alpha=0.8)

    # # ax.bar(df['Time'].astype(str), df['Geely'], bottom=df['LiAuto'] + df['BMW'],label='Geely',color=['w','w','b'],alpha=0.8)



    ax.set_xlabel('Week')

    ax.set_ylabel('%')

    ax.set_title(chooseM+' Uptime')

    ax.legend(loc='center',bbox_to_anchor=(1.2,0.5))

 

    plt.xticks(bar['Week1'].astype(str),rotation=90,size=8)

    # y=[0,0.2,0.4,0.6,0.8,1,1.2]

    # plt.yticks(range(len(y)),y)


      # 在次坐标轴上绘制折线图

    plt.twinx()

    # ls:线的类型，lw：宽度

    plt.plot(bar.iloc[:,0].astype(str), bar.iloc[:,19], ls='--', lw=2, color='r', marker='d',ms = 20, mfc = 'm', label='农村与城镇的消费占比')


    # 设置次坐标轴的取值范围，避免折线图波动过大，这里默认显示

    plt.ylim(0,8)

    st.pyplot(fig)

if charttype=="by day":

    colist=[]

    lablelistsu=['Excute','Idle','Stopped','Suspended','Aborted','Starting','Stopping','Aborting','Holding','Held','Unholding','Suspending','Unsuspending','Resetting','Completing','Complete','Clearing','Turnoff','Changover']

    colist.append('Day1')

    colist=colist+lablelistsu

    bar=pd.DataFrame(columns=colist)

    kl=0

    for i in range(dfbase.index[0],dfbase.index[0]+len(dfbase.loc[:,'date']),2):

        bar.loc[kl,'Day1']=dfbase.loc[i,'date'].date()

        temlist=[]

        for j in range(1,len(lablelistsu)+1):

            if j==len(lablelistsu):

                temlist=[dfbase.iloc[i-dfbase.index[0],j+3],dfbase.iloc[i-dfbase.index[0]+1,j+3]]

                bar.iloc[kl,j]=np.mean(temlist)

            else:

                temlist=[dfbase.iloc[i-dfbase.index[0],j+1],dfbase.iloc[i-dfbase.index[0]+1,j+1]]

                bar.iloc[kl,j]=np.mean(temlist)

        kl=kl+1


    colorS=['g','y','r','c','m','SeaGreen','OrangeRed','SteelBlue','LightSkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Aqua','DarkTurquoise','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen','g','y','r','c','m','SeaGreen']

    bottomS=bar.iloc[:,1]

    fig, ax = plt.subplots(figsize=(8, 6))

    alphaS=[0.5,0.6,0.7]

    bar_plot1=ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,1],label=bar.columns[1],color=colorS[0])

    for rect,i in zip(bar_plot1,range(len(bar.iloc[:,1]))):

        height_1=bar.iloc[i,1]

        ax.text(rect.get_x() + rect.get_width()/2., height_1-0.08, "%.2f" % height_1,

                ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')


    ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,2],bottom=bottomS,label=bar.columns[2],color=colorS[1])

    for rect,ih in zip(bar_plot1,range(len(bar.iloc[:,2]))):

        if bar.iloc[ih,2]>0.1:

            height_1h=bar.iloc[ih,2]+bar.iloc[ih,1]

            ax.text(rect.get_x() + rect.get_width()/2., height_1h-0.08, "%.2f" % bar.iloc[ih,2],

                    ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')


    #bar.shape[1]-1

    for isa in range(3,bar.shape[1]-1):

        for k in range(isa,isa+1):

          bottomS=bottomS+ bar.iloc[:,isa-1]

        ax.bar(bar.iloc[:,0].astype(str), bar.iloc[:,isa],bottom=bottomS,label=bar.columns[isa],color=colorS[isa-1])

        for rect,ik in zip(bar_plot1,range(len(bar.iloc[:,isa]))):

            if bar.iloc[ik,isa]>0.1:

                height_1k=0

                for su in range(1,isa+1):

                    height_1k=height_1k+bar.iloc[ik,su]

                ax.text(rect.get_x() + rect.get_width()/2., height_1k-0.05, "%.2f" % bar.iloc[ik,isa],

                        ha='center', va='bottom', fontsize=10, color='black', fontname='Times New Roman')

    # ax.bar(df['Time'].astype(str), df['LiAuto'],label='LiAuto',color=['r','w','w'],alpha=0.8)

    # ax.bar(df['Time'].astype(str), df['BMW'], bottom=df['LiAuto'], label='BMW',color=['w','g','w'],alpha=0.8)

    # ax.bar(df['Time'].astype(str), df['Geely'], bottom=df['LiAuto'] + df['BMW'],label='Geely',color=['w','w','b'],alpha=0.8)






    ax.set_xlabel('Day')

    ax.set_ylabel('%')

    ax.set_title(chooseM+' Uptime')

    ax.legend(loc='center',bbox_to_anchor=(1.2,0.5))


 

     

    # y=[0,0.2,0.4,0.6,0.8,1,1.2]

    # plt.yticks(range(len(y)),y)

    plt.xticks(bar['Day1'].astype(str),rotation=90,size=8)


      # 在次坐标轴上绘制折线图

    plt.twinx()

    # ls:线的类型，lw：宽度

    plt.plot(bar.iloc[:,0].astype(str), bar.iloc[:,19], ls='--', lw=2, color='r', marker='d',ms = 20, mfc = 'm', label='农村与城镇的消费占比')


    # 设置次坐标轴的取值范围，避免折线图波动过大，这里默认显示

    plt.ylim(0,12)

    st.pyplot(fig)


 

 

 

#summary Pie

piechart=[]

lablechart=[]

for c in bar.columns:

    if c=="Week1" or c=="Day1" or c=="Changover":

        continue

    else:

        if bar[c].mean()>0:#sum(dfbase.loc[:,c])>0:

            piechart.append(bar[c].mean())

            lablechart.append(c)

# lablelist=['Excute','Idle','Stopped','Suspended','Aborted','Starting','Stopping','Aborting','Holding','Held','Unholding','Suspending','Unsuspending','Resetting','Completing','Complete','Clearing']

colors=['g','y','r','c','m','SeaGreen','OrangeRed','SteelBlue','LightSkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Aqua','DarkTurquoise']

# index_list = [i for i, x in enumerate(pielist) if x == 0]

# while len(index_list)>0:

#     del pielist[index_list[0]]

#     del lablelist[index_list[0]]

#     del colors[index_list[0]]

#     index_list = [i for i, x in enumerate(pielist) if x == 0]

fig = plt.figure(figsize=(8, 6))

plt.pie(piechart, labels=lablechart, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90, radius=1.5)

plt.legend(loc="best")

plt.axis('equal') # 设置x和y轴的刻度相等，去掉周围的标记符号

plt.show()

# st.write('Summary Pie '+chooseM)

st.subheader('Summary Pie '+chooseM)

# st.header('Summary Pie '+chooseM)

# st.title('')

st.pyplot(plt)
