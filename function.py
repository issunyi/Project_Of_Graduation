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
def get_df_from_db(sql):
    db = pymysql.connect(host="localhost", user="root", passwd="sun010628", db="practice")
    cursor = db.cursor()  # 使用cursor()方法获取用于执行SQL语句的游标
    cursor.execute(sql)  # 执行SQL语句
    """
    使用fetchall函数以元组形式返回所有查询结果并打印出来
    fetchone()返回第一行，fetchmany(n)返回前n行
    游标执行一次后则定位在当前操作行，下一次操作从当前操作行开始
    """
    data = cursor.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = cursor.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df

    """
    使用完成之后需关闭游标和数据库连接，减少资源占用,cursor.close(),db.close()
    db.commit()若对数据库进行了修改，需进行提交之后再关闭
    """
    cursor.close()
    db.close()

    # print("cursor.description中的内容：", columnDes)
    return df

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





