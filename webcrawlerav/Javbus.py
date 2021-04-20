#-*-coding:utf-8-*-

import downloader
import pageparser
import controler


def get_dict(url):
    """get the dict of the detail page and yield the dict"""
    url_html = downloader.get_html(url)
    for detail_url in pageparser.parser_homeurl(url_html):
        try:
            detail_page_html = downloader.get_html(detail_url)
            dict_jav = pageparser.parser_content(detail_page_html)
        except:
            with open('fail_url.txt', 'a') as fd:
                fd.write('%s\n' % detail_url)
            print("Fail to crawl %s\ncrawl next detail page......" % detail_url)
            continue
        yield dict_jav, detail_url

def join_db(url,is_uncensored):
    """the detail_dict of the url join the db"""
    for dict_jav_data, detail_url in get_dict(url):
        if controler.check_url_not_in_csv(dict_jav_data['URL']):
            controler.write_data_csv(dict_jav_data, is_uncensored)
            print(dict_jav_data)
            print("Crawled %s" % detail_url)
        else:
            print('This %s date already in table' % dict_jav_data['avid'])

def main(entrance):

    #创建数据表
    controler.create_csv()
    is_uncensored = 1
    #只爬首页
    join_db(entrance, is_uncensored)
    #爬后面的10页
'''
    num = 0
    entrance_html = downloader.get_html(entrance)
    next_page_url = pageparser.get_next_page_url(entrance, entrance_html)
    while True:
        if next_page_url:
            join_db(next_page_url,is_uncensored)
        next_page_html = downloader.get_html(next_page_url)
        next_page_url = pageparser.get_next_page_url(entrance, next_page_html)
        num +=1
        if next_page_url == None:
            break
        if num > 10:
            break

'''
if __name__ == '__main__':
    main('https://www.javbus.com')


