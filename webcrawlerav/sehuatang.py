#-*-coding:utf-8-*-
import sqlite3
from bs4 import BeautifulSoup
from lxml import etree
import time

import downloader
import csv
import codecs
import sys
import random

sqlpath=r'./database/'
dbname = r'sht.sqlite3.db'

isProxy = False

def create_csv():
    with codecs.open('./database/sht.csv', 'w','utf-8') as f:
        fieldnames = {'avid', 'URL', 'magnetuploadtime','title','coverimage','magnet','detail',}  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.close()
    print("csv created successfully")

def create_db():
    '''create a db and table if not exists'''
    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()

    query = "CREATE TABLE IF NOT EXISTS SHT_DATA(avid   TEXT    PRIMARY KEY,URL  TEXT,title     TEXT," \
            "coverimage      TEXT,magnet    TEXT," \
            "magnetuploadtime    TEXT,detail    TEXT);"


    cursor.execute(query)
    print("Table created successfully")
    cursor.close()
    conn.commit()
    conn.close()

def crawlpage(url = ''):
    join_db(url)


def parser_content_xpath(avid, htmll, link):

    strhtml = htmll
    result = etree.HTML(strhtml)

    categories = {}

    categories['URL'] = link
    categories['coverimage'] = ''
    categories['detail'] = ''
    categories['magnetuploadtime'] = ''

    magnet = str(result.xpath(".//ol/li/text()")[0])
    categories['magnet'] = magnet

    linerow1 = result.xpath(".//p[@class='xg1 y']/span/@title")
    linerow2 = result.xpath(".//p[@class='xg1 y']/text()")

    if (linerow1):
        categories['magnetuploadtime'] = linerow1[0]
    if (linerow2):
        categories['magnetuploadtime'] = linerow2[0]



    linerow = result.xpath('.//td[@class="t_f"]/text()')
    i =0
    for lil in linerow:
        rowt = str(lil)
        categories['detail'] += rowt.replace('       ','')
        if i == 12:
            break
        i += 1


    img1 = result.xpath(".//img[contains(@id ,'aimg')]/@file")[0]
    img2 = result.xpath(".//img[contains(@id ,'aimg')]/@file")[1]

    categories['coverimage'] = img1 + "||" + img2

    categories['title'] = avid[1]

    categories['avid'] = avid[0]

    return categories


#处理每个番号的子页，
def parser_content(avid,html,link):

    soup = BeautifulSoup(html, "html.parser")

    categories = {}
    categories['avid'] = avid[0]
    categories['title'] = avid[1]
    alink = soup.find('ol')
    categories['magnet'] = alink.li.text
    categories['URL'] = link
    categories['发行日期'] = ''
    categories['长度'] = ''
    categories['导演'] = ''
    categories['制作商'] = ''
    categories['发行商'] = ''
    categories['系列'] = ''
    categories['类别'] = ''
    categories['演员'] = ''
    categories['coverimage'] = ''

    #categories = getDMMinfo(avid,categories)

    return categories
def get_detilepage(link):
    detail_page_html = downloader.get_html_txt(link,isProxy)
    dict_jav = parser_content_xpath('', detail_page_html, link)
    print(dict_jav)

def get_dict(homeurl,url,topitem):
    """get the dict of the detail page and yield the dict"""
    url_html = downloader.get_html(url,isProxy)
    i = 0
    for item in parser_homeurl(url_html):


        if i < topitem:
            i += 1
            continue

        print(item)
        if check_url_not_in_table(item[1][0]) == False:
            continue


        st = random.randint(1, 4)
        time.sleep(st)
        try:
            link = f'{homeurl}{item[0]}'
            detail_page_html = downloader.get_html_txt(link,isProxy)

            dict_jav = parser_content_xpath(item[1],detail_page_html,link)
            print("xpath 解析数据成功！")
        except:
            row = f'{item[1][0]},{link}\n'
            with open('fail_url.csv', 'a') as fd:
                fd.write(row)
            print("Fail to crawl %s\ncrawl next detail page......" % link)
            continue
        i += 1
        yield dict_jav, item

def parser_homeurl(html):
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('a', attrs={"class": "s xst"}):
        avid = item.text.split(" ",1)
        if len(avid) > 1 :
            yield item['href'],avid
        else :
            continue

def write_data(dict_jav, uncensored):
    '''write_data(dict_jav, uncensored)'''
    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()
    #dict_jav = getDMMinfo(dict_jav['avid'],dict_jav)
    if dict_jav == None :
        return

    #{'avid', 'URL', 'magnetuploadtime', 'title', 'coverimage', 'magnet', 'detail', }
    insert_data = (dict_jav['avid'], dict_jav['URL'], dict_jav['magnetuploadtime'],
                   dict_jav['title'], dict_jav['coverimage'],
                       dict_jav['magnet'], dict_jav['detail'],)
    #插入数据
    cursor.execute('''
    INSERT INTO SHT_DATA (avid, URL, magnetuploadtime, title, coverImage, magnet,detail)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)

    cursor.close()
    conn.commit()
    conn.close()

def join_db(homeurl,url,topitem):
    for dict_jav_data, detail_url in get_dict(homeurl,url,topitem):
        #if check_url_not_in_table(detail_url[1][0]):
        if check_url_not_in_table(detail_url[1][0]):
            print(dict_jav_data)
            #write_data(dict_jav_data, 1)
            write_data(dict_jav_data, 1)
            print("Crawled %s" % detail_url[0])
        else:
            print('This %s date already in table' % dict_jav_data['avid'])

def write_data_csv(dict_jav, uncensored):
    with codecs.open('./database/sht.csv', 'a','utf-8') as f:
        fieldnames = {'avid', 'URL','magnetuploadtime','title','coverimage','magnet','detail',}  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(dict_jav)
        f.close()


def check_url_not_in_csv(avid):

    return True
    f = codecs.open('./database/sht.csv', 'r', 'utf-8')
    reader = csv.DictReader(f)
    f.close()
    for row in reader:
        if row['avid'] == avid:
            return False
    return True



def check_url_not_in_table(avid):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""
    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()

    cursor.execute('select avid from SHT_DATA where avid=?', (avid,))
    check = cursor.fetchall()
    cursor.close()
    conn.close()
    if check:
        return False

    return True

def textxpath():

    dict_jav = parser_content_xpath(None,'', None)
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    create_db()

    #textxpath()
    #create_csv()

    homeurll = r'https://www.sehuatang.net/'

    if len(sys.argv) < 2:
        url = r'https://www.sehuatang.net/forum-37-1.html'
        join_db(homeurll,url,2)
        for i in range(2,11):
            st = random.randint(2, 15)
            time.sleep(st)
            url = f'https://www.sehuatang.net/forum-37-{i}.html'
            join_db(homeurll,url,0)
    else :
        url = sys.argv[1]
        get_detilepage(url)
