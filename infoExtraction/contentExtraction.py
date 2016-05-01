#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import bs4
sys.path.append("..")
import requests
import re
import random
import time
import MySQLdb

db = MySQLdb.connect("localhost", "root", "123123", "sinaSpider",charset="utf8")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
cursor.execute("SET NAMES utf8")
cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
db.commit()

loop = True
while loop:
    import url.URLOperation
    result = url.URLOperation.SelectURL(0)
    if not result:
        loop = False
        break
    URLId = result[0]
    url = result[1]
    print url
    cookie = {
        'M_WEIBOCN_PARAMS':'uicode%3D20000174',
        'uicode%3D20000174':'1461984033',
        'SSOLoginState':'1462100669',
        'SUB': '_2A256IZLtDeRxGeRG61QZ9SrPzjmIHXVZ7T6lrDV6PUJbstBeLUP8kW1LHet-WQo-R0Q8lNuy_F5q7QeahGPtcg..',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5rCy9rOuUMQ4H7f72NDKv15JpX5o2p',
        'SUHB': '0ElaSFZ5qrQrgN',
        '_T_WM': 'a7f9a84b9eab75edc5748c9d9383e581',
        'gsid_CTandWM': '4ussCpOz5Hh7b2qnoOY1PbMbQ5J'
    }
    html = requests.get(url, cookies=cookie).content
    soup = bs4.BeautifulSoup(html)

    contentList = soup.select('div.c')
    if not contentList:
        loop =False
        print "error in cookie"

    for divs in contentList:
        try:
            divs['id']
        except:
            continue
        userId = 0
        userName = ''
        weiboContent = ''
        extraInfo = ''
        posts = 0
        repeats = 0
        agrees = 0
        loopTime = 1
        for div in divs.find_all('div'):
            if(loopTime == 1):
                try:
                    userName = div.find('a', 'nk').string
                    userUrl = div.find('a','nk')['href']
                    import url.URLOperation
                    url.URLOperation.StoreURL(userUrl,2)
                    print userUrl
                    userId =  re.search('weibo.cn(.*)\/(.*)',userUrl).group(2)
                except:
                    continue

                if div.find('span','ctt'):
                    weiboContent = str(div.find('span', 'ctt'))
                    weiboContent = re.sub(r'</?\w+[^>]*>', '', weiboContent)
                if div.find('span', 'ct'):
                    extraInfo = div.find('span', 'ct').string
                otherInfo = re.findall('\[(\d+)\]', str(div))
                if otherInfo:
                    posts = otherInfo[2]
                    repeats = otherInfo[1]
                    agrees = otherInfo[0]
            if loopTime == 2:
                if div.find('span', 'ct'):
                    extraInfo = div.find('span','ct').string
                otherInfo = re.findall('\[(\d+)\]', str(div))
                if otherInfo:
                    posts = otherInfo[2]
                    repeats = otherInfo[1]
                    agrees = otherInfo[0]
                if str(div).find('转发理由') != -1:
                    weiboContent = re.sub(r'</?\w+[^>]*>', '', str(div))
            if loopTime ==3:
                if div.find('span', 'ct'):
                    extraInfo = div.find('span', 'ct').string
                otherInfo = re.findall('\[(\d+)\]', str(div))
                if otherInfo:
                    posts = otherInfo[2]
                    repeats = otherInfo[1]
                    agrees = otherInfo[0]
                if str(div).find('转发理由') != -1:
                    weiboContent = re.sub(r'</?\w+[^>]*>', '', str(div))
            loopTime = loopTime + 1

        weiboContent = weiboContent.replace(':', '')
        print userId
        print userName
        print weiboContent
        print extraInfo
        print posts
        print repeats
        print agrees

        sql = "INSERT INTO weiboInfo (userId,context,posts,repeats,agrees,extraInfo) " \
              "VALUES ('%s','%s','%s','%s','%s','%s')" % (userId,(weiboContent),posts,repeats,agrees,(extraInfo))
        print sql
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print 'insert weiboInfo success'
        except:
            # Rollback in case there is any error
            db.rollback()
            print "insert weiboInfo fail"

    import url.URLOperation
    if soup.find('div','pa').form.div.a.string == '下页':
        nextPage = "http://weibo.cn" + soup.find('div', 'pa').form.div.a['href']
        url.URLOperation.StoreURL(nextPage,0)
    url.URLOperation.UpdateURL(URLId)

    randomTime = random.uniform(1,5)
    time.sleep(randomTime)