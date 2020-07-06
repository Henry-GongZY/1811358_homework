import pymysql
import pandas as pd
conn = pymysql.connect(host="localhost", user="root", password="", database="user_comments")
cursor = conn.cursor()
sql='select content from user_comments.user_comments'
cursor.execute(sql)
curr=cursor.fetchall()   #从数据库拿出爬虫爬取到的数据,通过抽取特定列实现评论抽取
comments=[]
for i in curr:
    comments.append(i[0].replace('\n','').replace('外形外观：','').replace('加热速度：','').replace('耗能情况：','').replace('其他特色：','').replace('洗浴时间：',''))
    #去除换行符以及京东评论区保持评论结构统一用到的分割字段
comments=pd.DataFrame(pd.Series(comments).unique())
    #去重，生成csv文件并进行下一步处理
comments.to_csv('comments.csv',encoding='utf-8',header=False)