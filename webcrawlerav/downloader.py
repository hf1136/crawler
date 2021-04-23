#-*-coding:utf-8-*-

import requests
import urllib3

urllib3.disable_warnings()

proxies = {'http': 'socks5h://127.0.0.1:7890',
           'https': 'socks5h://127.0.0.1:7890'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
}
def save_html(html,filename):
     with open(f'./html/test.html','w','utf-8') as f:
         f.write(html)
         f.close()
     print("html file saved successfully")

def get_html(url, Referer_url=None):
    '''get_html(url),download and return html'''
    req = ''
    if Referer_url:
        headers['Referer'] = Referer_url
    try:
        req = requests.get(url, headers=headers,proxies=proxies,verify=False)
        print("get data from %s" % url)
        #save_html(req.content, url)
        req.close()
        return req.content
    except:
        print("Sorry requests can not connect host")
        return None



def get_html_txt(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers,proxies=proxies,verify=False)
    print ("get data from %s" % url)
    req.close()
    return req.text

def get_html_noprox(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers,verify=False)
    print ("get data from %s" % url)
    return req.content

def get_html_noprox_text(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers,verify=False)
    print ("get data from %s" % url)
    return req.text


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