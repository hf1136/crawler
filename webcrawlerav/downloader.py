#-*-coding:utf-8-*-

import requests
import urllib3

urllib3.disable_warnings()

proxies = {'http': 'socks5://127.0.0.1:7890',
           'https': 'socks5://127.0.0.1:7890'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
}

def get_html(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers,proxies=proxies,verify=False)
    print ("get data from %s" % url)
    req.close()
    return req.content

def get_html_noprox(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers,verify=False)
    print ("get data from %s" % url)
    return req.content

def get_html_cookie(url, cookies):
    '''get_html(url),download and return html'''
    req = requests.get(url, headers=headers,cookies=cookies,proxies=proxies,verify=False)
    print ("get cookie data from %s" % url)
    return req.content

def post_data_cookie(url, cookies=None,datas=None, files=None):
    '''post_data(url),download and return html'''
    req = requests.post(url, headers=headers,cookies=cookies,data=datas, files=files,proxies=proxies,verify=False)
    print ("post data with cookie to %s" % url)
    return req