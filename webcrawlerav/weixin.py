#-*-coding:utf-8-*-
import downloader
import requests
from http.cookiejar import Cookie, MozillaCookieJar

def load_cookies_from_mozilla():
    ns_cookiejar = MozillaCookieJar()
    ns_cookiejar.load("./data/cookie", ignore_discard=True, ignore_expires=True)
    return ns_cookiejar

if __name__ == '__main__':

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    cookie = load_cookies_from_mozilla()


    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }

    token = 103622428
    data = {
        "token": "103622428",
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": 0,
        "count": "5",
        "query": "",
        "fakeid": "MzA3ODAwNzIyOQ==",
        "type": "9",
    }

    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        print(item["title"])

