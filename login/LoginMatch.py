#coding=utf-8
import re
import json
def sServerData(serverData):#解析得到serverTime，nonce等
    "Search the server time & nonce from server data"
    p = re.compile('\((.*)\)') #re.compile 可以把正则表达式编译成一个正则表达式对象
    jsonData = p.search(serverData).group(1) #查找
    data = json.loads(jsonData) #对encodedjson进行decode，得到原始数据，需要使用json.loads()函数
    serverTime = str(data['servertime'])
    nonce = data['nonce']
    pubkey = data['pubkey']#
    rsakv = data['rsakv']#
    print "Server time is:", serverTime
    print "Nonce is:", nonce
    return serverTime, nonce, pubkey, rsakv