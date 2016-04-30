#coding=utf-8
import cookielib
import re
import urllib2
import LoginEncode
import LoginMatch

class WeiboLogin:

    def __init__(self,user,pwd,enableProxy = False):
        print "Initializing sinaLogin"
        self.username = user
        self.password = pwd
        self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)"
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        self.cookiejar = cookielib.MozillaCookieJar('cookie.txt')  # 建立cookie
        self.cookiejar.save()
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def Login(self):
        print "logining..."

        cookie_support = urllib2.HTTPCookieProcessor(self.cookiejar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)  # 构建cookie对应的opener

        serverTime,nonce,pubkey,rsakv = self.GetServerTime()
        postData = LoginEncode.PostEncode(self.username, self.password, serverTime, nonce, pubkey, rsakv)  # 加密用户和密码
        print "Post data length:", len(postData)

        req = urllib2.Request(self.loginUrl, postData, self.postHeader)  # 构造网络请求
        print "Posting request..."
        result = urllib2.urlopen(req)  # 发出网络请求
        self.cookiejar.save()

        text = result.read()
        # print unicode(text,'gbk')

        p = re.compile('location\.replace\([\'"](.*?)[\'"]')
        try:
            login_url = p.search(text).group(1)
            # 由于之前的绑定，cookies信息会直接写入
            urllib2.urlopen(login_url)
            self.cookiejar.save()
            print "Login success!"
            return True
        except:
            print 'Login error!'
            return False

    def GetServerTime(self):
        print "Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl).read()  # 得到网页内容
        print serverData
        try:
            serverTime, nonce, pubkey, rsakv = LoginMatch.sServerData(serverData)  # 解析得到serverTime，nonce等
            return serverTime, nonce, pubkey, rsakv
        except:
            print 'Get server time & nonce error!'
            return None

if __name__ == '__main__':
    weiboLogin = WeiboLogin('469464794@qq.com', '*****')  # 邮箱（账号）、密码
    if(weiboLogin.Login()):
        print '登录成功'
    myurl = "http://weibo.com/u/2806854355/home"
    htmlContent = urllib2.urlopen(myurl).read()
    print htmlContent.find('判断首页是否有我的昵称')#