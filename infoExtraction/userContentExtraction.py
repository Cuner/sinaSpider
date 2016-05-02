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
    result = url.URLOperation.SelectURL(2)
    if not result:
        loop = False
        break
    URLId = result[0]
    url = result[1]
    userId = re.search('weibo.cn(.*)\/(.*)', url).group(2)
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

    try:
        fanNum = ''
        userId = ''
        userName = ''
        userRecog = ''
        userLocation = ''
        userGender = ''
        userSummary = ''

        # 保存用户信息
        tips = str(soup.find('div','tip2'))
        fanNum = re.search('粉丝\[(\d+)\]'.encode('utf8'),tips.encode('utf8')).group(1)
        userInfo = str(soup.find('div', 'ut'))
        userUrl = 'http://weibo.cn' + re.search('<a\shref="(\/\d+\/info)">资料'.encode('utf8'),userInfo.encode('utf8')).group(1)
        userHtml = requests.get(userUrl, cookies=cookie).content
        userId = re.search('\/(\d+)\/',userUrl).group(1)
        if re.search('>昵称:(.*?)<'.encode('utf8'),userHtml.encode('utf8')):
            userName = re.search('>昵称:(.*?)<'.encode('utf8'),userHtml.encode('utf8')).group(1)
        if re.search('>认证:(.*?)<'.encode('utf8'), userHtml.encode('utf8')):
            userRecog = re.search('>认证:(.*?)<'.encode('utf8'), userHtml.encode('utf8')).group(1)
        if re.search('>地区:(.*?)<'.encode('utf8'), userHtml.encode('utf8')):
            userLocation = re.search('>地区:(.*?)<'.encode('utf8'), userHtml.encode('utf8')).group(1)
        if re.search('>性别:(.*?)<'.encode('utf8'), userHtml.encode('utf8')):
            userGender = re.search('>性别:(.*?)<'.encode('utf8'), userHtml.encode('utf8')).group(1)
        if re.search('>简介:(.*?)<'.encode('utf8'), userHtml.encode('utf8')):
            userSummary = re.search('>简介:(.*?)<'.encode('utf8'), userHtml.encode('utf8')).group(1)
        if userGender == '女':
            userGender = 1
        else:
            userGender = 0
        print fanNum
        print userId
        print userName
        print userRecog
        print userLocation
        print userGender
        print userSummary

        sql = "INSERT INTO userInfo (userId,userName,fanNum,userRecog,location,gender,summary) " \
              "VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (userId, userName, fanNum, userRecog, userLocation, userGender,userSummary)
        print sql
        cursor.execute(sql)
        db.commit()
        print 'insert userInfo success'
    except:
        userInfo = str(soup.find('div','ut'))
        userName = re.search('class="ut">(.*?)的微博'.encode('utf8'),userInfo.encode('utf8')).group(1)

    contentList = soup.select('div.c')
    if not contentList:
        loop =False
        print "error in cookie"

    for divs in contentList:
        try:
            divs['id']
        except:
            continue
        weiboContent = ''
        extraInfo = ''
        posts = 0
        repeats = 0
        agrees = 0
        loopTime = 1
        for div in divs.find_all('div'):
            if(loopTime == 1):
                if div.find('span','ctt'):
                    weiboContent = str(div.find('span', 'ctt'))#微博正文
                    weiboContent = re.sub(r'</?\w+[^>]*>', '', weiboContent)
                if div.find('span', 'ct'):
                    extraInfo = div.find('span', 'ct').string#发布时间以及来源
                otherInfo = re.findall('\[(\d+)\]', str(div))
                if len(otherInfo)>3:
                    posts = otherInfo[2]#微博评论数
                    repeats = otherInfo[1]#微博转发数
                    agrees = otherInfo[0]#微博点赞数
            if loopTime == 2:
                if div.find('span', 'ct'):
                    extraInfo = div.find('span','ct').string
                otherInfo = re.findall('\[(\d+)\]', str(div))
                if len(otherInfo)>3:
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
    try:
        if soup.find('div','pa').form.div.a.string == '下页':
            nextPage = "http://weibo.cn" + soup.find('div', 'pa').form.div.a['href']
            url.URLOperation.StoreURL(nextPage,2)
            print nextPage
    except:
        print "No next page"
    url.URLOperation.UpdateURL(URLId)

    randomTime = random.uniform(1,3)
    time.sleep(randomTime)