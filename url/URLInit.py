# encoding: utf-8
import urllib
import URLOperation

def init_url(keyWord):
    print keyWord

    origin_url_content = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + urllib.quote(keyWord)
    print origin_url_content
    origin_url_user = "http://weibo.cn/search/user/?keyword=" + urllib.quote(keyWord)
    origin_url_tag = "http://weibo.cn/search/user/?keyword=" + urllib.quote(keyWord) + "&stag=" + urllib.quote("搜标签")

    URLOperation.StoreURL(origin_url_content, 0)
    URLOperation.StoreURL(origin_url_user, 1)
    URLOperation.StoreURL(origin_url_tag, 1)

if __name__ == '__main__':
    init_url("武汉大学")