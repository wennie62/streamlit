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
#sys.path.append('C:\\ProgramData\\Anaconda3\\lib\\site-packages')
from PIconnect import PI
with PI.PIServer() as server:
    print(server.server_name)
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

def utc2local( utc_dtm ):
    # UTC 时间转本地时间（ +8:00 ）
    local_tm = datetime.datetime.fromtimestamp( 0 )
    utc_tm = datetime.datetime.utcfromtimestamp( 0 )
    offset = local_tm - utc_tm
    return utc_dtm + offset





def outputd(tagmame,Starttime,Endtime):
    parameter_names=[tagmame]

    for i in range(len(parameter_names)):
        
        paras = {'start_time': Starttime.strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': Endtime.strftime('%Y-%m-%d %H:%M:%S'),
                 'boundary_type':'inside',
    #             'filter_expression':"parameter!='Bad'"
                 }
        df=pd.DataFrame(columns=[]) 
        with PI.PIServer() as server:
            point = server.search(parameter_names[i])[0]
            value = point.recorded_values(**paras) #PI里面的数据
            df=value.to_frame() #PI的数据转换成dataframe
    
     
    
     
    
        df['Time']=df.index 
        df['Time']=utc2local(df.index)
        df.reset_index(drop=True)
        df['Time'] = df['Time'].dt.tz_localize(None)     
        df[parameter_names[i]]=df[parameter_names[i]].astype('str') 
        df=df.replace('Bad','')
        df=df[df[parameter_names[i]]!='']
        df[parameter_names[i]]=df[parameter_names[i]].str.replace('_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0','')
        df=df.sort_values(['Time'],ascending=[1]).reset_index(drop=True)
        df[parameter_names[i]]=df[parameter_names[i]].astype('float')
        df['Status_Count']=1
        df['Cuttime']=''
        count=1
        for j in df.index.tolist()[1:]:
            if df[parameter_names[i]][j-1]!=df[parameter_names[i]][j]:
                count=count+1
            df.loc[j,'Status_Count']=count
        
        
        
        
    # -*- coding: utf-8 -*-
    """
    Created on Thu Aug 17 16:18:53 2023
    
     
    
    @author: gux9
    """
    if len(df)<3:
        pielist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dffi=pd.DataFrame()
    if len(df)>2:
    
        dffi = pd.DataFrame()
        dfdelt=pd.DataFrame()
        looplist=df.index.tolist()
        looplist.pop()
        for g in looplist:
            if df.loc[g,tagmame]==6:
                task="Excute"
            if df.loc[g,tagmame]==4:
                task="Idle"
            if df.loc[g,tagmame]==2:
                task="Stopped"
            if df.loc[g,tagmame]==5:
                task="Suspended"
            if df.loc[g,tagmame]==9:
                 task="Aborted"
            if df.loc[g,tagmame]==3:
                 task="Starting"
            if df.loc[g,tagmame]==7:
                 task="Stopping"
            if df.loc[g,tagmame]==8:
                 task="Aborting"
            if df.loc[g,tagmame]==10:
                 task="Holding"
            if df.loc[g,tagmame]==11:
                 task="Held"
            if df.loc[g,tagmame]==12:
                 task="Unholding"
            if df.loc[g,tagmame]==13:
                 task="Suspending"
            if df.loc[g,tagmame]==14:
                 task="Unsuspending"
            if df.loc[g,tagmame]==15:
                 task="Resetting"
            if df.loc[g,tagmame]==16:
                 task="Completing"
            if df.loc[g,tagmame]==17:
                 task="Complete"
            if df.loc[g,tagmame]==1:
                  task="Clearing"
            
            delttime=(df.iloc[g+1,1]-df.iloc[g,1]).total_seconds()   
            dictdelt=dict(Resource=task,Duratime=delttime)
            dfdelt = dfdelt.append(dictdelt, ignore_index=True, sort=False)
            dicts=dict(Task=str(g), Start=str(df.loc[g,'Time']), Finish=str(df.loc[g+1,'Time']), Resource=task)
            dffi = dffi.append(dicts, ignore_index=True, sort=False)
        pielist=[]
        lablelist=[]
        lablelistsu=['Excute','Idle','Stopped','Suspended','Aborted','Starting','Stopping','Aborting','Holding','Held','Unholding','Suspending','Unsuspending','Resetting','Completing','Complete','Clearing','Turnoff']
        for i in range(len(lablelistsu)):
            if sum(dfdelt[dfdelt['Resource']==lablelistsu[i]]['Duratime'])>0:
                pielist.append(sum(dfdelt[dfdelt['Resource']==lablelistsu[i]]['Duratime'])/12/60/60)
            else:
                pielist.append(0)
    return pielist,dffi


   # 
     
def cuttime(tagmameC,tagnamere,Starttime,Endtime):
    parameter_names1=[tagname]

    for i in range(len(parameter_names1)):
        
        paras = {'start_time': Starttime.strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': Endtime.strftime('%Y-%m-%d %H:%M:%S'),
                 'boundary_type':'inside',
    #             'filter_expression':"parameter!='Bad'"
                 }
        df1=pd.DataFrame(columns=[]) 
        with PI.PIServer() as server:
            point = server.search(parameter_names1[i])[0]
            value = point.recorded_values(**paras) #PI里面的数据
            df1=value.to_frame() #PI的数据转换成dataframe
    
     
    
        df1['Time']=df1.index 
        df1['Time']=utc2local(df1.index)
        df1.reset_index(drop=True)
        df1['Time'] = df1['Time'].dt.tz_localize(None)     
        df1[parameter_names1[i]]=df1[parameter_names1[i]].astype('str') 
        df1=df1.replace('Bad','')
        df1=df1[df1[parameter_names1[i]]!='']
        df1[parameter_names1[i]]=df1[parameter_names1[i]].str.replace('_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0','')
        df1=df1.sort_values(['Time'],ascending=[1]).reset_index(drop=True)
        df1[parameter_names1[i]]=df1[parameter_names1[i]].astype('float')
    
        df1['sheet_Count']=1
        df1['recipe']=''
        count=1
        for j in df1.index.tolist()[1:]:
            if df1[parameter_names1[i]][j-1]>df1[parameter_names1[i]][j]:
                count=count+1
            df1.loc[j,'sheet_Count']=count

        
        parameter_names2=[tagnamere]

        for ii in df1['sheet_Count'].drop_duplicates().tolist():
             if len(df1[df1['sheet_Count']==ii]['Time'])<2:
                 continue
             df2=pd.DataFrame(columns=[]) 
             Endtime2 = df1[df1['sheet_Count']==ii]['Time'].max().strftime('%Y-%m-%d %H:%M:%S')
             Starttime2 = df1[df1['sheet_Count']==ii]['Time'].min().strftime('%Y-%m-%d %H:%M:%S')    
    
      
    
      
    
         
             paras = {'start_time': Starttime2,
                      'end_time': Endtime2 ,
                      'boundary_type':'inside',
                      }
    
    
             with PI.PIServer() as server:
                 point = server.search(parameter_names2[i])[0]
                 value = point.recorded_values(**paras) #PI里面的数据
                 df2=value.to_frame() #PI的数据转换成dataframe
    
             if len(df2.index)==0:
                 continue
             df2['Time']=df2.index 
             df2['Time']=utc2local(df2.index)
             df2.reset_index(drop=True)
             df2['Time'] = df2['Time'].dt.tz_localize(None)     
             df2[parameter_names2[i]]=df2[parameter_names2[i]].astype('str') 
             df2=df2.replace('Bad','')
             df2=df2[df2[parameter_names2[i]]!='']
             df2=df2.drop_duplicates([parameter_names2[i]], keep='first')
             df1.loc[df1[df1['sheet_Count']==ii].index,'recipe']=''.join(df2[parameter_names2[i]].values.tolist())
        
        dfr=df1[df1['recipe']!='']
        dfr=dfr.dropna()
        dfr=dfr.drop_duplicates(['recipe'], keep='last')
        dfr=dfr.drop(columns=['Time'])
        dfr=dfr.drop(columns=['sheet_Count'])
        dfr=pd.DataFrame(dfr,columns=['recipe',tagname])
        dfr.style.set_properties(**{'background-color': 'black','color': 'green'})
        
        
        # import openpyxl as op
        # from datetime import datetime
        # workbook=op.load_workbook('C:\\Users\\jiangw14\\Documents\\Status\\recipe.xlsx')
        # sheet=workbook.active
        #df1[(df1['recipe'].notnull) & (df1['recipe'] != "")]
        dfkan=pd.DataFrame()
        row=len(df1)
        if row<10:
            changeovercount=0
        else:
            if df1.iloc[0][3]:
                temp_recipe=df1.iloc[0][3]
            else:
                temp_recipe="None"
            dfkan.loc[0,0]=''
            dfkan.loc[0,1]=temp_recipe
            #sheet.cell(row=1,column=2,value=temp_recipe)
            count_start=df1.iloc[0][2]
            excel_row=0
            flag=1
            if df1.iloc[0][3]:
                indexlist=df1[(df1['recipe']!="")].index.tolist()[1:]
            else:
                indexlist=df1[(df1['recipe']!="")].index.tolist()
            for row_index in indexlist: 
                if df1.iloc[row_index-1][3] =="" and df1.iloc[row_index][3] != "":
                    excel_row += 1
                    count_end=df1.iloc[row_index][2]
                    end_time=df1.iloc[row_index][1]
                    temp_recipe=df1.iloc[row_index+1][3]
                    dfkan.loc[excel_row,excel_row]=count_end-count_start
                    dfkan.loc[excel_row,0]=end_time
                    dfkan.loc[0,excel_row+1]=temp_recipe
                    # sheet.cell(row=excel_row,column=excel_row,value=count_end-count_start)  
                    # sheet.cell(row=excel_row,column=1,value=end_time)
                    # sheet.cell(row=1,column=excel_row+1,value=temp_recipe)
                    count_start=count_end
                    markrow=row_index
            if (len(df1[(df1['recipe']!="")].index.tolist())==0):
                dfkan.loc[excel_row+1,0]=df1.values[-1][1]
                dfkan.loc[excel_row+1,excel_row+1]=df1.values[-1][2]-count_start
            else:
                dfkan.loc[excel_row+1,0]=df1.values[-1][1]
                reci_name=df1.iloc[row_index,3]
                reci_tolist=(dfr[dfr['recipe']==reci_name][tagname]).tolist()
                dfkan.loc[excel_row+1,excel_row+1]=df1.values[-1][2]-count_start+df1.values[-1][0]/reci_tolist[0]
            
            changeovercount=dfkan.shape[1]-1
    
        return changeovercount

     # 

def onsite(tagname,tagnamere,Starttime,Endtime):
    parameter_names1=[tagname]

    for i in range(len(parameter_names1)):
        
        paras = {'start_time': Starttime.strftime('%Y-%m-%d %H:%M:%S'),
                 'end_time': Endtime.strftime('%Y-%m-%d %H:%M:%S'),
                 'boundary_type':'inside',
    #             'filter_expression':"parameter!='Bad'"
                 }
        df1=pd.DataFrame(columns=[]) 
        with PI.PIServer() as server:
            point = server.search(parameter_names1[i])[0]
            value = point.recorded_values(**paras) #PI里面的数据
            df1=value.to_frame() #PI的数据转换成dataframe
    
     
    
        df1['Time']=df1.index 
        df1['Time']=utc2local(df1.index)
        df1.reset_index(drop=True)
        df1['Time'] = df1['Time'].dt.tz_localize(None)     
        df1[parameter_names1[i]]=df1[parameter_names1[i]].astype('str') 
        df1=df1.replace('Bad','')
        df1=df1[df1[parameter_names1[i]]!='']
        df1[parameter_names1[i]]=df1[parameter_names1[i]].str.replace('_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0','')
        df1=df1.sort_values(['Time'],ascending=[1]).reset_index(drop=True)
        df1[parameter_names1[i]]=df1[parameter_names1[i]].astype('float')
    
        df1['sheet_Count']=1
        df1['recipe']=''
        count=1
        for j in df1.index.tolist()[1:]:
            if df1[parameter_names1[i]][j-1]>df1[parameter_names1[i]][j]:
                count=count+1
            df1.loc[j,'sheet_Count']=count

        
        parameter_names2=[tagnamere]

        for ii in df1['sheet_Count'].drop_duplicates().tolist():
             if len(df1[df1['sheet_Count']==ii]['Time'])<2:
                 continue
             df2=pd.DataFrame(columns=[]) 
             Endtime2 = df1[df1['sheet_Count']==ii]['Time'].max().strftime('%Y-%m-%d %H:%M:%S')
             Starttime2 = df1[df1['sheet_Count']==ii]['Time'].min().strftime('%Y-%m-%d %H:%M:%S')    
    
      
    
      
    
         
             paras = {'start_time': Starttime2,
                      'end_time': Endtime2 ,
                      'boundary_type':'inside',
                      }
    
    
             with PI.PIServer() as server:
                 point = server.search(parameter_names2[i])[0]
                 value = point.recorded_values(**paras) #PI里面的数据
                 df2=value.to_frame() #PI的数据转换成dataframe
    
             if len(df2.index)==0:
                 continue
             df2['Time']=df2.index 
             df2['Time']=utc2local(df2.index)
             df2.reset_index(drop=True)
             df2['Time'] = df2['Time'].dt.tz_localize(None)     
             df2[parameter_names2[i]]=df2[parameter_names2[i]].astype('str') 
             df2=df2.replace('Bad','')
             df2=df2[df2[parameter_names2[i]]!='']
             df2=df2.drop_duplicates([parameter_names2[i]], keep='first')
             df1.loc[df1[df1['sheet_Count']==ii].index,'recipe']=''.join(df2[parameter_names2[i]].values.tolist())
        
        dfr=df1[df1['recipe']!='']
        dfr=dfr.dropna()
        dfr=dfr.drop_duplicates(['recipe'], keep='last')
        dfr=dfr.drop(columns=['Time'])
        dfr=dfr.drop(columns=['sheet_Count'])
        dfr=pd.DataFrame(dfr,columns=['recipe',tagname])
        dfr.style.set_properties(**{'background-color': 'black','color': 'green'})
        df130=dfr[dfr[tagname] > 10]  
        
        # import openpyxl as op
        # from datetime import datetime
        # workbook=op.load_workbook('C:\\Users\\jiangw14\\Documents\\Status\\recipe.xlsx')
        # sheet=workbook.active
        #df1[(df1['recipe'].notnull) & (df1['recipe'] != "")]
        dfkan=pd.DataFrame()
        row=len(df1)
        if row<10:
            changeovercount=0
        else:
            if df1.iloc[0][3]:
                temp_recipe=df1.iloc[0][3]
            else:
                temp_recipe="None"
            dfkan.loc[0,0]=''
            dfkan.loc[0,1]=temp_recipe
            #sheet.cell(row=1,column=2,value=temp_recipe)
            count_start=df1.iloc[0][2]
            excel_row=0
            flag=1
            if df1.iloc[0][3]:
                indexlist=df1[(df1['recipe']!="")].index.tolist()[1:]
            else:
                indexlist=df1[(df1['recipe']!="")].index.tolist()
            for row_index in indexlist: 
                if df1.iloc[row_index-1][3] =="" and df1.iloc[row_index][3] != "":
                    excel_row += 1
                    count_end=df1.iloc[row_index][2]
                    end_time=df1.iloc[row_index][1]
                    temp_recipe=df1.iloc[row_index+1][3]
                    dfkan.loc[excel_row,excel_row]=count_end-count_start
                    dfkan.loc[excel_row,0]=end_time
                    dfkan.loc[0,excel_row+1]=temp_recipe
                    # sheet.cell(row=excel_row,column=excel_row,value=count_end-count_start)  
                    # sheet.cell(row=excel_row,column=1,value=end_time)
                    # sheet.cell(row=1,column=excel_row+1,value=temp_recipe)
                    count_start=count_end
                    markrow=row_index
            if (len(df1[(df1['recipe']!="")].index.tolist())==0):
                dfkan.loc[excel_row+1,0]=df1.values[-1][1]
                dfkan.loc[excel_row+1,excel_row+1]=df1.values[-1][2]-count_start
            else:
                dfkan.loc[excel_row+1,0]=df1.values[-1][1]
                reci_name=df1.iloc[row_index,3]
                reci_tolist=(dfr[dfr['recipe']==reci_name][tagname]).tolist()
                dfkan.loc[excel_row+1,excel_row+1]=df1.values[-1][2]-count_start+df1.values[-1][0]/reci_tolist[0]
            
            changeovercount=dfkan.shape[1]-1
            colname=['Time']
            for shape1 in range(1,dfkan.shape[1]):
                colname.append(dfkan.iloc[0,shape1])
            refkan=pd.DataFrame(columns=colname)
            for shape0 in range(0,dfkan.shape[0]-1):
                refkan.loc[shape0,'Time']=dfkan.loc[shape0+1,0]
            for shape0 in range(1,dfkan.shape[0]):
                refkan.iloc[shape0-1:dfkan.shape[0]-1,shape0]=dfkan.loc[shape0,shape0]
                if shape0>1:
                    refkan.iloc[0:shape0-1,shape0]=0 
    return df130, refkan


st.title('Start Your Fantastic Data Journey')

st.header('Cutter Utilization Summary')

cycle1=("Cutter 105","Cutter 107","Cutter 108")
chooseM=st.selectbox('Please Select the Cutter Number',cycle1)


dfbase105=pd.read_excel(r'Cutter\\datebase105.xlsx')
dfbase107=pd.read_excel(r'Cutter\\datebase107.xlsx')
dfbase108=pd.read_excel(r'Cutter\\datebase108.xlsx')
dfbase105['date'] = pd.to_datetime(dfbase105['date'])
indexfirszero=(dfbase105.loc[dfbase105['Week1'] == 0].index.tolist())[0]

# filter1=datetime.datetime(2023, 7, 15, 20, 30,00)
# testendtim=datetime.datetime(2023, 7, 20, 8, 30,00)
di=0
if filter2<dfbase105.iloc[indexfirszero-1,0]:
    di=1
else:
    date_write=dfbase105.iloc[indexfirszero-1,0]
    for i in range(0,1000,2):
        date_write=date_write+timedelta(1)
        dfbase105.iloc[indexfirszero+i,0]=date_write
        dfbase105.iloc[indexfirszero+i,1]='D'
        
        Date=date_write.date()
        Time1= datetime.time(8, 30,00)
        Time2= datetime.time(20, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC105.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        for lo in range(18):
            dfbase105.iloc[indexfirszero+i,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase105.iloc[indexfirszero+i,20]=week
        dfbase105.iloc[indexfirszero+i,21]=Starttime.month
        tagnameC='HFWR.XYC105.EQUIP_CUTTME'
        tagnamere='HFWR.XYC105.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase105.iloc[indexfirszero+i,22]=lendf130
        
        
        dfbase105.iloc[indexfirszero+i+1,0]=date_write
        dfbase105.iloc[indexfirszero+i+1,1]='N'
        Date=date_write.date()
        Time1= datetime.time(20, 30,00)
        Time2= datetime.time(8, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Date=Date+timedelta(1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC105.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        
        for lo in range(18):
            dfbase105.iloc[indexfirszero+i+1,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase105.iloc[indexfirszero+i+1,20]=week
        dfbase105.iloc[indexfirszero+i+1,21]=Starttime.month
        tagnameC='HFWR.XYC105.EQUIP_CUTTME'
        tagnamere='HFWR.XYC105.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase105.iloc[indexfirszero+i+1,22]=lendf130
        if date_write.date()>=filter2.date():
            break
    
    date_write=dfbase107.iloc[indexfirszero-1,0]
    for i in range(0,1000,2):
        date_write=date_write+timedelta(1)
        dfbase107.iloc[indexfirszero+i,0]=date_write
        dfbase107.iloc[indexfirszero+i,1]='D'
        
        Date=date_write.date()
        Time1= datetime.time(8, 30,00)
        Time2= datetime.time(20, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC107.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        for lo in range(18):
            dfbase107.iloc[indexfirszero+i,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase107.iloc[indexfirszero+i,20]=week
        dfbase107.iloc[indexfirszero+i,21]=Starttime.month
        tagnameC='HFWR.XYC107.EQUIP_CUTTME'
        tagnamere='HFWR.XYC107.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase107.iloc[indexfirszero+i,22]=lendf130
        
        
        dfbase107.iloc[indexfirszero+i+1,0]=date_write
        dfbase107.iloc[indexfirszero+i+1,1]='N'
        Date=date_write.date()
        Time1= datetime.time(20, 30,00)
        Time2= datetime.time(8, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Date=Date+timedelta(1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC107.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        
        for lo in range(18):
            dfbase107.iloc[indexfirszero+i+1,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase107.iloc[indexfirszero+i+1,20]=week
        dfbase107.iloc[indexfirszero+i+1,21]=Starttime.month
        tagnameC='HFWR.XYC105.EQUIP_CUTTME'
        tagnamere='HFWR.XYC105.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase107.iloc[indexfirszero+i+1,22]=lendf130
        if date_write.date()>=filter2.date():
            break
    
    date_write=dfbase108.iloc[indexfirszero-1,0]
    for i in range(0,1000,2):
        date_write=date_write+timedelta(1)
        dfbase108.iloc[indexfirszero+i,0]=date_write
        dfbase108.iloc[indexfirszero+i,1]='D'
        
        Date=date_write.date()
        Time1= datetime.time(8, 30,00)
        Time2= datetime.time(20, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC108.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        for lo in range(18):
            dfbase108.iloc[indexfirszero+i,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase108.iloc[indexfirszero+i,20]=week
        dfbase108.iloc[indexfirszero+i,21]=Starttime.month
        tagnameC='HFWR.XYC108.EQUIP_CUTTME'
        tagnamere='HFWR.XYC108.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase108.iloc[indexfirszero+i,22]=lendf130
        
        
        dfbase108.iloc[indexfirszero+i+1,0]=date_write
        dfbase108.iloc[indexfirszero+i+1,1]='N'
        Date=date_write.date()
        Time1= datetime.time(20, 30,00)
        Time2= datetime.time(8, 30,00)
        Starttime=datetime.datetime.combine(Date, Time1)
        Date=Date+timedelta(1)
        Endtime=datetime.datetime.combine(Date, Time2)
        tagname='HFWR.XYC108.EQUIP_STAT'
        pielist,dffi=outputd(tagname,Starttime,Endtime)
        
        for lo in range(18):
            dfbase108.iloc[indexfirszero+i+1,lo+2]=pielist[lo]
        year, week, week_day = Starttime.isocalendar()
        dfbase108.iloc[indexfirszero+i+1,20]=week
        dfbase108.iloc[indexfirszero+i+1,21]=Starttime.month
        tagnameC='HFWR.XYC105.EQUIP_CUTTME'
        tagnamere='HFWR.XYC105.EQUIP_RECIPE'
        lendf130=cuttime(tagnameC,tagnamere,Starttime,Endtime)
        dfbase108.iloc[indexfirszero+i+1,22]=lendf130
        if date_write.date()>=filter2.date():
            break
    
    
    
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
st.subheader('Gantt Chart '+chooseM)
# st.write('Gantt Chart '+chooseM)
# st.header('Gantt Chart '+chooseM)
# st.title('甘特图')
# GanD=st.date_input('选定日期', datetime.date(2023, 7, 19))
# GanT=st.time_input('选定日期', datetime.time(20,30,0,0))
Col1, Col2 = st.columns(2)
GanD=Col1.date_input('Choose Date', datetime.date(2023, 7, 19))
GanT=Col2.time_input('Choose Time', datetime.time(20,30,0,0))
filterGan= datetime.datetime.combine(GanD, GanT)
Ftitle = Col1.text_input('Movie Forward', '12')
Btitle = Col2.text_input('Movie Back', '12')
if len(Ftitle)>0:
    Starttime=filterGan-datetime.timedelta(hours=int(Ftitle), minutes=0, seconds=0)
    Endtime=filterGan
    pielist,dffi=outputd(tagname,Starttime,Endtime)
else:
    if len(Btitle)>0:
        Starttime=filterGan-datetime.timedelta(hours=int(Btitle), minutes=0, seconds=0)
        Endtime=filterGan
        pielist,dffi=outputd(tagname,Starttime,Endtime)
    else:
        Starttime=filterGan-datetime.timedelta(hours=12, minutes=0, seconds=0)
        Endtime=filterGan
        pielist,dffi=outputd(tagname,Starttime,Endtime)

# filter2= datetime.datetime.combine(date1, time1)
if dffi.shape[0]>0:
    fig1 = px.timeline(dffi, x_start="Start", x_end="Finish", y="Resource", color="Resource")
    st.plotly_chart(fig1)






# 主栏


Starttime=filter2-datetime.timedelta(hours=12, minutes=0, seconds=0)
Endtime=filter2
dfp,dfc = onsite(tagnameC,tagnamere,Starttime,Endtime)
Col3, Col4 = st.columns(2)
fixtime = Col3.text_input('Please Input buffer Time(s)', '12')


dfp[tagnameC]=np.where(dfp[tagnameC]>0,dfp[tagnameC]+int(fixtime),0)
st.write("### CT Data By Cutter"+chooseM, dfp.sort_index())
printy=Col4.button('Print to C:\\Cutter\\')
if printy:
   dfp.to_excel("Cutter\\CT"+chooseM+".xlsx") 
    

colorsumaey=['SeaGreen','DarkSeaGreen','SteelBlue','LightSkyBlue','SkyBlue','DeepSkyBlue','LightBLue','PowDerBlue','CadetBlue','PaleTurquoise','Cyan','Aqua','DarkTurquoise']
colorS=[]
bottomS=dfc.iloc[:,1]
fig, ax = plt.subplots(figsize=(8, 6))
alphaS=[1,1,1,1,1,1,1,1,1,1,1,1]
for i in range(dfc.shape[1]-1):
    if i>0:
        for c in range(dfc.shape[1]-1):
            colorS.append('w')
        colorS[i]=colorsumaey[i]
        if i>1:
              for k in range(i,i+1):
                bottomS=bottomS+ dfc.iloc[:,i]
        ax.bar(dfc.iloc[:,0].astype(str), dfc.iloc[:,i+1],bottom=bottomS,label=dfc.columns[i+1],color=colorS,alpha=alphaS[i])
    else:
        for c in range(dfc.shape[1]-1):
            colorS.append('w')
        colorS[i]=colorsumaey[i]
        bar_plot2=ax.bar(dfc.iloc[:,0].astype(str), dfc.iloc[:,i+1],label=dfc.columns[i+1],color=colorS,alpha=alphaS[i])

    for rect,ic in zip(bar_plot2,range(len(dfc.iloc[:,i]))):
        if dfc.iloc[ic,i+1]>0.1:
            height_1k=0
            for su in range(1,i+1):
                height_1k=height_1k+dfc.iloc[ic,su]
            ax.text(rect.get_x() + rect.get_width()/2., height_1k-0.05, "%.1f" % dfc.iloc[ic,i+1],
                    ha='center', va='bottom', fontsize=10, color='white', fontname='Times New Roman')
# ax.bar(df['Time'].astype(str), df['LiAuto'],label='LiAuto'

# ax.bar(df['Time'].astype(str), df['LiAuto'],label='LiAuto',color=['r','w','w'],alpha=0.8)
# ax.bar(df['Time'].astype(str), df['BMW'], bottom=df['LiAuto'], label='BMW',color=['w','g','w'],alpha=0.8)
# ax.bar(df['Time'].astype(str), df['Geely'], bottom=df['LiAuto'] + df['BMW'],label='Geely',color=['w','w','b'],alpha=0.8)

 

 

ax.set_xlabel('Time')
ax.set_ylabel('Pcs')
ax.set_title(chooseM+' Pcs Over Time')
ax.legend()
leg = ax.get_legend()
k=0
for i in leg.legendHandles:
    i.set_color(colorsumaey[k])
    # i.set_markeredgecolor(colorsumaey[k])
    k=k+1
 

 

plt.xticks(dfc['Time'].astype(str),rotation=90,size=8)
topcs=0
for tot in range (1,dfc.shape[1]):
    topcs=topcs+dfc.iloc[dfc.shape[1]-2,tot]
st.write("### Total PCs "+chooseM,int(topcs))

# 在Streamlit中显示图表
st.pyplot(fig)
st.balloons()
# def get_data():
#     file = r'C:\Cutter\CTS_workcount.xlsx'
#     return pd.read_excel(file)
# dfp= get_data()
# print(values)

 

# dfp=dfp[dfp['recipe']!='']
# dfp=dfp.dropna()
# dfp=dfp.drop_duplicates(['recipe'], keep='last')
# dfp=dfp.drop(columns=['Time'])
# dfp=dfp.drop(columns=['sheet_Count'])
# dfp=pd.DataFrame(dfp,columns=['recipe','HFWR.XYC105.EQUIP_CUTTME'])
# dfp.style.set_properties(**{'background-color': 'black','color': 'green'})
# dfp30=dfp[dfp['HFWR.XYC105.EQUIP_CUTTME'] > 30]

 


 






