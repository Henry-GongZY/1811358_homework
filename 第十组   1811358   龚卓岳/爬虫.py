import json
import pymysql
import requests
import time
import re
import random
import urllib
import pymongo


def get_comments_number():
    url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=100004771217'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    html = response.text
    comments_count = re.findall('\"CommentCount\":(.*?),.*?\"DefaultGoodCount\":(.*?),', html, re.S)
    return int(comments_count[0][0]) - int(comments_count[0][1])


def get_comments(__url):
    # myclient = pymongo.MongoClient("mongodb://localhost:127.0.0.1:27017/")
    # mydb = myclient["user_comments"]
    # mycol = mydb["sites"]
    __html = urllib.request.urlopen(__url).read().decode('gbk', 'ignore')
    data0 = re.sub(u'^fetchJSON_comment98\(', '', __html)  # re.sub即利用正则替换想替换的内容
    reg = re.compile('\);')
    data0 = reg.sub('', data0)
    data = json.loads(data0)
    print(type(data))
    # 如果匹配不到comments,content，则返回1,否则返回0\n",
    # judge=re.findall('.*?\\\"content\\\".*?',data,re.S)
    # if len(judge)==0:
    #    return 1
    for i in data['comments']:
        Id = i['id']
        content = i['content']
        date_time = i['creationTime']
        write_to_mysql(str(Id), content, date_time)
        print(Id, content, date_time)
        # mycol.insert_one(i)

def write_to_mysql(Id, content, date_time):
    conn = pymysql.connect(host="localhost", user="root", password="", database="user_comments")
    cursor = conn.cursor()
    sql = "insert into user_comments values( \"%s\", \"%s\", \"%s\")" % (Id, content, date_time)
    cursor.execute(sql)
    cursor.connection.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100004771217" \
          "&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
    num = get_comments_number()
    print(num)
    for i in range(0, int(num / 10)):
        print("正在获取第{}页评论数据!".format(i + 1))
        url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100004771217' \
              '&score=0&sortType=5&page=' + str(i) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
        print(url)
        get_comments(url)
        # 设置休眠时间
        time.sleep(random.randint(1, 3))