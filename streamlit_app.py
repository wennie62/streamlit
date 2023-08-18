# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:00:46 2023

@author: jiangw14
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import datetime
# 侧边栏
st.sidebar.title('请选择过滤条件')
time = st.sidebar.time_input('大于时间', datetime.time(1,0))
#day = st.sidebar.time_inpt('大于日期', datetime.day(1,0))

# # values = st.sidebar.slider('速度',0.0, 200.0, (25.0, 75.0))
# # 主栏
# st.title('数据探索')
# # @st.cache(persist=True)
# def get_data():
#     file = r'CTS_workcount.xlsx'
#     return pd.read_csv(file, header=0)
# df = get_data()
# # # print(values)
# # df = data[data['Time'] > str(time)]

 

# fig, ax = plt.subplots(figsize=(8, 6))

 

# ax.bar(df['Time'], df['LiAuto'], label='LiAuto')
# ax.bar(df['Time'], df['BMW'], bottom=df['LiAuto'], label='BMW')
# ax.bar(df['Time'], df['Geely'], bottom=df['LiAuto'] + df['BMW'], label='Value3')

 

# ax.set_xlabel('Time')
# ax.set_ylabel('Value')
# ax.set_title('Stacked Bar Chart')
# ax.legend()

 

# plt.xticks(df['Time'])

 

# # 在Streamlit中显示图表
# st.pyplot(fig)


# def get_data():
#     file = r'CTS_workcount.xlsx'
#     return pd.read_excel(file)
# df1 = get_data()
# # print(values)

 

# df1=df1[df1['recipe']!='']
# df1=df1.dropna()
# df1=df1.drop_duplicates(['recipe'], keep='last')
# df1=df1.drop(columns=['Time'])
# df1=df1.drop(columns=['sheet_Count'])
# df1=pd.DataFrame(df1,columns=['recipe','HFWR.XYC105.EQUIP_CUTTME'])
# df1.style.set_properties(**{'background-color': 'black','color': 'green'})

 

st.write("### CT Data By Cutter ($105)", df1.sort_index())
