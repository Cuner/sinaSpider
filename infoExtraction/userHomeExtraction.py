#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import bs4
sys.path.append("..")
import requests
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
    result = url.URLOperation.SelectURL(1)
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

    tableList = soup.select('table')
    if not tableList:
        loop =False
        print "error in cookie"

    for table in tableList:
        userUrl =  'http://weibo.cn' + table.find('tr').a['href']
        import url.URLOperation
        result = url.URLOperation.StoreURL(userUrl,2)
    import url.URLOperation
    if soup.find('div', 'pa').form.div.a.string == '下页':
        nextPage = "http://weibo.cn" + soup.find('div', 'pa').form.div.a['href']
        url.URLOperation.StoreURL(nextPage, 1)
        print nextPage
    url.URLOperation.UpdateURL(URLId)