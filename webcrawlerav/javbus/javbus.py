#-*-coding:utf-8-*-
import sys
import time

import pageparser
import controler
import downloader

isProxy = False

def get_dict(url):
    """get the dict of the detail page and yield the dict"""
    url_html = downloader.get_html(url,Referer_url=None,isproxy=isProxy)
    for detail_url in pageparser.parser_homeurl(url_html):
        if controler.check_url_not_in_table(detail_url) == False:
            continue
        try:
            detail_page_html = downloader.get_html(detail_url,Referer_url=None,isproxy=isProxy)
            dict_jav = pageparser.parser_content(detail_page_html,isProxy)
        except:
            with open('fail_url.txt', 'a') as fd:
                fd.write('%s\n' % detail_url)
            print("Fail to crawl %s\ncrawl next detail page......" % detail_url)
            continue
        yield dict_jav, detail_url

def join_db(url,is_uncensored):
    """the detail_dict of the url join the db"""
    for dict_jav_data, detail_url in get_dict(url):
        time.sleep(3)
        if controler.check_url_not_in_table(dict_jav_data['URL']):
            print(dict_jav_data)
            controler.write_data(dict_jav_data, is_uncensored)
            print("Crawled %s" % detail_url)
        else:
            print('This %s date already in table' % dict_jav_data['avid'])

def test_parser():
    # detail_url = 'https://www.javbus.com/AGAV-054'
    # detail_page_html = downloader.get_html_txt(detail_url)
    #
    # print(type(detail_page_html))
    # with open('tt.html', 'w', encoding='utf-8') as f:
    #     f.write(detail_page_html)
    # f.close()

    f = open("./tt.html", "r",encoding='utf-8')
    str = f.read()
    detail_page_html = str
    f.close()

    dict_jav = pageparser.parser_content(detail_page_html)


def main(entrance):

    #创建数据表
    controler.create_db()
    is_uncensored = 1
    #只爬首页
    #join_db(entrance, is_uncensored)
    #爬后面的10页
    #test_parser()

    num = 0
    entrance_html = downloader.get_html(entrance,Referer_url=None,isproxy=isProxy)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url,is_uncensored)
        next_page_html = downloader.get_html(next_page_url,Referer_url=None,isproxy=isProxy)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        num +=1
        if next_page_url == None:
            break
        if num > 150:
            break


if __name__ == '__main__':
    main('https://www.javbus.com/')


