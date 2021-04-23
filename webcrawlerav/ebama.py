# -*-coding:utf-8-*-
from lxml import etree
import time

import downloader
import csv
import codecs


##########################################

def create_csv():
    with codecs.open('./database/ebama.csv', 'w', 'utf-8') as f:
        fieldnames = {'avid', 'URL', 'title', '发行日期', '长度', '导演', '制作商', '发行商', '系列', '演员', '类别', 'coverimage',
                      'magnet', 'torrentname', 'torrenthash', }  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.close()
    print("csv created successfully")




def crawlpage(url=''):
    join_db(url)


def parser_content_xpath(avid, html, link):
    # html = etree.parse('./html/test.html', etree.HTMLParser())

    result = etree.HTMLParser(html)
    # result = etree.parse(html, etree.HTMLParser())

    # response = html.xpath('//*')
    magnet = result.xpath(".//ol/li/text()")
    # avinfo = html.xpath('.//table[@cellspacing="0"][@cellpadding="0"]')
    avinfo = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')

    # categories = {}
    # categories['avid'] = avid[0]
    # categories['title'] = avid[1]
    line1 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[0]
    line2 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[1]
    line3 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[2]
    line4 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[3]
    line5 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[4]
    line6 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[5]
    line7 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[6]
    line8 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[7]
    line9 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[8]
    line10 = result.xpath('.//td[@class="t_f"][@id="postmessage_4204385"]/text()')[9]

    i = 0
    for li in avinfo:
        if i == 0:
            avid = li.decode('Shift_JIS')
        print(i)
        print(li)
        i += 1

    # title = html.xpath(".//title/text()")
    # keywords = html.xpath('//meta[@name="keywords"]/@content')
    #
    # avid = html.xpath('//div[@class="col-md-3 info"]/p[1]/span[2]/text()')
    # issuedate = html.xpath('//div[@class="col-md-3 info"]/p[2]/text()')
    # length = html.xpath('//div[@class="col-md-3 info"]/p[3]/text()')




def get_dict(homeurl, url, topitem):
    """get the dict of the detail page and yield the dict"""
    url_html = downloader.get_html_noprox_text(url)
    i = 0
    for item in parser_homeurl(url_html):
        time.sleep(5)
        print(item)
        if i < topitem:
            i += 1
            continue
        # try:
        link = f'{homeurl}{item[0]}'
        # detail_page_html = downloader.get_html(link)
        detail_page_html = downloader.get_html_txt(link)

        # dict_jav = parser_content(item[1],detail_page_html,link)
        dict_jav = parser_content_xpath(item[1], detail_page_html, link)
        # except:
        #     #with open('fail_url.txt', 'a') as fd:
        #     #    fd.write('%s\n' % item)
        #     print("Fail to crawl %s\ncrawl next detail page......" % link)
        #     continue
        i += 1

        yield dict_jav, item


def parser_homeurl(html):
    aaa = etree.HTML(html)

    magnet = aaa.xpath(".//ol/li/text()")


    print(result)

    # soup = BeautifulSoup(html, "html.parser")
    # for item in soup.find_all('a', attrs={"class": "s xst"}):
    #     avid = item.text.split(" ", 1)
    #     if len(avid) > 1:
    #         yield item['href'], avid
    #     else:
    #         continue



def join_db(homeurl, url, topitem):
    for dict_data, detail_url in get_dict(homeurl, url, topitem):
        # if check_url_not_in_table(detail_url[1][0]):
        if check_url_not_in_csv(detail_url[1][0]):
            print(dict_data)
            # write_data(dict_jav_data, 1)
            write_data_csv(dict_data, 1)
            print("Crawled %s" % detail_url[0])
        else:
            print('This %s date already in table' % dict_jav_data['avid'])


def write_data_csv(dict_jav, uncensored):
    with codecs.open('./database/ebama.csv', 'a', 'utf-8') as f:
        fieldnames = {'avid', 'URL', 'title', '发行日期', '长度', '导演', '制作商', '发行商', '系列', '演员', '类别', 'coverimage',
                      'magnet', 'torrentname', 'torrenthash', }  # 表头
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # writer.writeheader()
        # print(dict_jav)
        writer.writerow(dict_jav)
        f.close()


def check_url_not_in_csv(avid):
    return True
    f = codecs.open('./database/ebama.csv', 'r', 'utf-8')
    reader = csv.DictReader(f)
    f.close()
    for row in reader:
        if row['avid'] == avid:
            return False
    return True




# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # create_db()

    # textxpath()

    create_csv()

    homeurll = r'https://www.xs8.cn/'
    #
    url = r'https://www.xs8.cn/rank/hotsales'
    join_db(homeurll, url, 0)
    #
    # url = r'https://www.sehuatang.net/forum-37-2.html'
    # join_db(homeurll,url,0)

    # crawlpage(url)
