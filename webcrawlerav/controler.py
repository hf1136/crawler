#-*-coding:utf-8-*-

import sqlite3
import csv
import codecs

sqlpath='./database/'
dbname = 'javbus.sqlite3.db'

#用来处理用Python的sqlite3操作数据库要插入的字符串中含有中文字符的时候报错处理，配合map
def _decode_utf8(aStr):
    return aStr.encode('utf-8','ignore').decode('utf-8')

def create_csv():
    with codecs.open('./database/javbus.csv', 'w','utf-8') as f:
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
        CREATE TABLE IF NOT EXISTS AV_DATA(
            avid      TEXT PRIMARY KEY,
            URL       TEXT,
            title     TEXT,
            發行日期  TEXT,
            長度      TEXT,
            導演      TEXT,
            製作商    TEXT,
            發行商    TEXT,
            系列      TEXT,
            演員      TEXT,
            類別      TEXT,
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

def write_data_csv(dict_jav, uncensored):
    def write_data_csv(dict_jav, uncensored):
        with codecs.open('./database/javbus.csv', 'a', 'utf-8') as f:
            fieldnames = {'avid', 'URL', 'title', '发行日期', '长度', '导演', '制作商', '发行商', '系列', '演员', '类别', 'coverimage',
                          'magnet', 'torrentname', 'torrenthash', }  # 表头
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # writer.writeheader()
            # print(dict_jav)
            writer.writerow(dict_jav)
            f.close()

def write_data(dict_jav, uncensored):
    '''write_data(dict_jav, uncensored)'''

    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()
    #对数据解码为unicode
    insert_data = map(_decode_utf8,
                      (dict_jav['avid'], dict_jav['URL'], dict_jav['title'],
                       dict_jav['發行日期'], dict_jav['長度'], dict_jav['導演'], dict_jav['製作商'],
                       dict_jav['發行商'], dict_jav['系列'], dict_jav['演員'], dict_jav['類別'],dict_jav['coverimage'],
                       dict_jav['magnet'], 'False', dict_jav['torrentname'], dict_jav['torrenthash'], 'NULL'))
    #insert_data.append(uncensored)
    #插入数据
    cursor.execute('''
    INSERT INTO AV_DATA (avid, URL, title, 發行日期, 長度, 導演, 製作商, 發行商, 系列, 演員, 類別, CoverImage,magnet, IsSeed, Torrentname, Torrenthash, Uploadcmd,)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)
    ''', insert_data)
    cursor.close()
    conn.commit()
    conn.close()

def check_url_not_in_csv(url):
    return True

def check_url_not_in_table(url):
    """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""

    conn = sqlite3.connect(sqlpath+dbname)
    cursor = conn.cursor()

    cursor.execute(f'select URL from AV_DATA where URL="{url}"')
    check = cursor.fetchall()
    cursor.close()
    conn.close()
    if check:
        return False
    return True