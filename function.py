# -*- coding: utf-8 -*-
# @Time : 2023/4/21 15:11
# @Author : sunyi
# @File : function.py
# @Software: PyCharm

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from colorama import Fore
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
from datetime import datetime, date
import warnings  # Supress warnings

import pymysql

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
np.random.seed(7)

def plot_total_active_power() :
    df = pd.read_csv("./data/environment_data.csv")
    print(df)
    sns.lineplot(x=df['date'], y=df['总有功功率（kw）'].fillna(method='ffill'), color='dodgerblue')
    plt.set_title('Feature: {}'.format('总有功功率（kw）'), fontsize=14)
    plt.set_ylabel(ylabel='总有功功率（kw）', fontsize=14)
    plt.set_xlim([date(2018, 1, 1), date(2018, 1, 15)])


# mysql数据库读取并转化为dataframe
def get_data():
    total_active_power = []
    highest_temp = []
    lowest_temp = []
    am_wind_toward = []
    pm_wind_toward = []
    weather_1 = []
    weather_2 = []

    date_time = []

    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='sun010628',
        db='test_users',
        charset='utf8'
    )
    # print("连接数据库成功")
    cur = conn.cursor()
    sql = "select * from data"
    cur.execute(sql)
    result = cur.fetchall()

    for item in result:
        date_time.append(item[0].strftime('%Y-%m-%d %H:%M:%S'))
        total_active_power.append(float(item[1]))
        highest_temp.append(float(item[2]))
        lowest_temp.append(float(item[3]))
        am_wind_toward.append(int(item[4]))
        pm_wind_toward.append(int(item[5]))
        weather_1.append(int(item[6]))
        weather_2.append(int(item[7]))

    mycursor = conn.cursor()
    mycursor.execute("SELECT MIN(date), MAX(date) FROM data")
    date_range = mycursor.fetchone()
    min_date = date_range[0].isoformat()
    max_date = date_range[1].isoformat()

    return total_active_power,highest_temp,lowest_temp,am_wind_toward,pm_wind_toward,weather_1,weather_2,min_date,max_date,date_time
    cur.close()
    conn.close()

# class connect_mysql_highest_temp(object):
#     def __init__(self):
#         try:
#             self.conn = pymysql.connect(host='localhost',user='root',password='sun010628',database='test_users',charset="utf8")
#             self.cursor = self.conn.cursor()  # 用来获得python执行Mysql命令的方法（游标操作）
#
#         except:
#
#
#     def getItems(self):
#         sql= "select HIGHEST_TEMP from data"    #获取food数据表的内容
#         self.cursor.execute(sql)
#         items = self.cursor.fetchall()  #接收全部的返回结果行
#         return items


if __name__ == "__main__":
    print('1')





