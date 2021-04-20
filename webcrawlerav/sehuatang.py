#-*-coding:utf-8-*-
import sqlite3
from bs4 import BeautifulSoup
import time

import downloader
import csv
import codecs

sqlpath=r'./database/'
dbname = r'sht.sqlite3.db'
##########################################

def create_csv():
    with codecs.open('./database/sht.csv', 'w','utf-8') as f:
        fieldnames = {'avid', 'URL', 'title','发行日期','长度','导演','制作商','发行商','系列','演员','类别','coverimage',
                      'magnet','torrentname','torrenthash',}  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.close()
    print("csv created successfully")

def create_db():
    '''create a db and table if not exists'''
    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SHT_DATA(
            avid      TEXT PRIMARY KEY,
            URL       TEXT,
            title     TEXT,
            发行日期  TEXT,
            长度      TEXT,
            导演      TEXT,
            制作商    TEXT,
            发行商    TEXT,
            系列      TEXT,
            演员      TEXT,
            类别      TEXT,
            CoverImage      TEXT,
            magnet    TEXT,
            IsSeed    TEXT,
            Torrentname    TEXT,
            Torrenthash    TEXT,
            Uploadcmd   TEXT,     
            无码      INTEGER);''')

    print("Table created successfully")
    cursor.close()
    conn.commit()
    conn.close()

def crawlpage(url = ''):
    join_db(url)

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
    categories['torrentname'] = ''
    categories['torrenthash'] = ''

    #categories = getDMMinfo(avid,categories)

    return categories

def get_dict(homeurl,url,topitem):
    """get the dict of the detail page and yield the dict"""
    url_html = downloader.get_html(url)
    i = 0
    for item in parser_homeurl(url_html):
        time.sleep(5)
        print(item)
        if i < topitem:
            i += 1
            continue
        try:
            link = f'{homeurl}{item[0]}'
            detail_page_html = downloader.get_html(link)
            dict_jav = parser_content(item[1],detail_page_html,link)
        except:
            #with open('fail_url.txt', 'a') as fd:
            #    fd.write('%s\n' % item)
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

def _decode_utf8(aStr):
    return aStr.encode('utf-8','ignore').decode('utf-8')




def write_data(dict_jav, uncensored):
    '''write_data(dict_jav, uncensored)'''
    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()
    #dict_jav = getDMMinfo(dict_jav['avid'],dict_jav)
    if dict_jav == None :
        return
    #对数据解码为unicode
    '''
    insert_data = map(_decode_utf8,
                      (dict_jav['avid'], dict_jav['URL'], dict_jav['title'],
                       dict_jav['发行日期'], dict_jav['长度'], dict_jav['导演'], dict_jav['制作商'],
                       dict_jav['发行商'], dict_jav['系列'], dict_jav['演员'], dict_jav['类别'], dict_jav['coverimage'],
                       dict_jav['magnet'], 'False', dict_jav['torrentname'], dict_jav['torrenthash'], ''))
    #insert_data.append(uncensored)
    '''
    insert_data = (dict_jav['avid'], dict_jav['URL'], dict_jav['title'],
                       dict_jav['发行日期'], dict_jav['长度'], dict_jav['导演'], dict_jav['制作商'],
                       dict_jav['发行商'], dict_jav['系列'], dict_jav['演员'], dict_jav['类别'], dict_jav['coverimage'],
                       dict_jav['magnet'], 'False', dict_jav['torrentname'], dict_jav['torrenthash'], '')
    #插入数据
    cursor.execute('''
    INSERT INTO SHT_DATA (avid, URL, title, 发行日期, 长度, 导演, 制作商, 发行商, 系列, 演员, 类别, CoverImage,magnet, IsSeed, Torrentname, Torrenthash, Uploadcmd)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', insert_data)

    cursor.close()
    conn.commit()
    conn.close()

def join_db(homeurl,url,topitem):
    for dict_jav_data, detail_url in get_dict(homeurl,url,topitem):
        #if check_url_not_in_table(detail_url[1][0]):
        if check_url_not_in_csv(detail_url[1][0]):
            print(dict_jav_data)
            #write_data(dict_jav_data, 1)
            write_data_csv(dict_jav_data, 1)
            print("Crawled %s" % detail_url[0])
        else:
            print('This %s date already in table' % dict_jav_data['avid'])

def write_data_csv(dict_jav, uncensored):
    with codecs.open('./database/sht.csv', 'a','utf-8') as f:
        fieldnames = {'avid', 'URL', 'title','发行日期','长度','导演','制作商','发行商','系列','演员','类别','coverimage',
                      'magnet','torrentname','torrenthash',}  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        #writer.writeheader()
        #print(dict_jav)
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

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    #create_db()
    create_csv()

    #url = r'https://www.sehuatang.net/forum-37-1.html'
    homeurll = r'https://www.sehuatang.net/'

    url = r'https://www.sehuatang.net/forum-37-1.html'
    join_db(homeurll,url,2)

    url = r'https://www.sehuatang.net/forum-37-2.html'
    join_db(homeurll,url,0)


    #crawlpage(url)
