import pymysql
import pandas as pd
conn = pymysql.connect(host="localhost", user="root", password="", database="user_comments")
cursor = conn.cursor()
sql='select content from user_comments.user_comments'
cursor.execute(sql)
curr=cursor.fetchall()
comments=[]
for i in curr:
    comments.append(i[0].replace('\n',''))
comments=pd.Series(comments)
print(comments)