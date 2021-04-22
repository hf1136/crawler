# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import downloader
import re
import math
import random


def _get_cili_url(htmltext):
    """get_cili(soup).get the ajax url and Referer url of request"""

    pattern7 = re.compile("var gid = (\d+)", re.S)
    matcher7 = pattern7.search(htmltext)
    pattern8 = re.compile("img = '(.*?)'", re.S)
    matcher8 = pattern8.search(htmltext)

    ajax_get_cili_url = ''
    if matcher7:
        gid = matcher7.group(1)
        img = matcher8.group(1)
        ajax_get_cili_url = "https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid={}&lang=zh&img={}&uc=0&floor={}".format(gid,
                                                                                                                   img,
                                                                                                                   math.floor(random.random()*1000+1))
    return ajax_get_cili_url


def _parser_magnet(html):
    """parser_magnet(html),get all magnets from a html and return the str of magnet"""

    # 存放磁力的字符串
    magnet = ''
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.select('td[width="70%"]'):
        if td.text.find(u'高清') != -1 :
            magnet += td.a['href'] + '||'
    return magnet

def _parser_torrentname(html):
    """parser_magnet(html),get all magnets from a html and return the str of magnet"""
    # 存放磁力的字符串
    magnet = ''
    soup = BeautifulSoup(html, "html.parser")
    ar = soup.text.split()
    tname = ''
    i = 0;
    for item in ar :
        if item == u'高清' :
            tname += ar[i-1] + '\n'
        i += 1
    return tname


def get_next_page_url(entrance, html):
    """get_next_page_url(entrance, html),return the url of next page if exist"""
    print("done the page.......")
    soup = BeautifulSoup(html, "html.parser")
    next_page = soup.select('a[id="next"]')
    if next_page:
        next_page_link = next_page[0]['href'].split('/')[-2:]
        next_page_link = '/' + '/'.join(next_page_link)
        next_page_url = entrance + next_page_link
        return next_page_url
    return None


def parser_homeurl(html):
    """parser_homeurl(html),parser every url on every page and yield the url"""

    soup = BeautifulSoup(html, "html.parser")
    for url in soup.select('a[class="movie-box"]'):
        if url.text.find(u'高清') > 0 :
            yield url['href']


def parser_content(htmltext):
    """parser_content(html),parser page's content of every url and yield the dict of content"""

    soup = BeautifulSoup(htmltext, "html.parser")
    pagetext = htmltext.decode('utf-8')

    categories = {}

    code_name_doc = soup.find('span', text="識別碼:")
    code_name = code_name_doc.parent.contents[2].text if code_name_doc else ''
    categories['avid'] = code_name
    # code_name = soup.find('span', text="識別碼:").parent.contents[2].text if soup.find('span', text="識別碼:") else ''

    categories['title'] = soup.title.text


    date_issue_doc = soup.find('span', text="發行日期:")
    date_issue = date_issue_doc.parent.contents[1].strip() if date_issue_doc else ''
    categories['發行日期'] = date_issue
    # date_issue = soup.find('span', text="發行日期:").parent.contents[1].strip() if soup.find('span', text="發行日期:") else ''

    duration_doc = soup.find('span', text="長度:")
    duration = duration_doc.parent.contents[1].strip() if duration_doc else ''
    categories['長度'] = duration
    # duration = soup.find('span', text="長度:").parent.contents[1].strip() if soup.find('span', text="長度:") else ''

    director_doc = soup.find('span', text="導演:")
    director = director_doc.parent.contents[2].text if director_doc else ''
    categories['導演'] = director
    # director = soup.find('span', text="導演:").parent.contents[2].text if soup.find('span', text="導演:") else ''

    manufacturer_doc = soup.find('span', text="製作商:")
    manufacturer = manufacturer_doc.parent.contents[2].text if manufacturer_doc else ''
    categories['製作商'] = manufacturer
    # manufacturer = soup.find('span', text="製作商:").parent.contents[2].text if soup.find('span', text="製作商:") else ''

    publisher_doc = soup.find('span', text="發行商:")
    publisher = publisher_doc.parent.contents[2].text if publisher_doc else ''
    categories['發行商'] = publisher
    # publisher = soup.find('span', text="發行商:").parent.contents[2].text if soup.find('span', text="發行商:") else ''

    series_doc = soup.find('span', text="系列:")
    series = series_doc.parent.contents[2].text if series_doc else ''
    categories['系列'] = series
    # series = soup.find('span', text="系列:").parent.contents[2].text if soup.find('span', text="系列:") else ''

    genre_doc = soup.find_all('span', class_="genre")
    genre_text = ''
    for i in genre_doc:
        fl = i.find('a')
        if fl :
            genre_text += '%s   ' % fl.text

    categories['類別'] = genre_text

    actor_doc = soup.select('span[onmouseover^="hoverdiv"]')
    actor = (i.text.strip() for i in actor_doc) if actor_doc else ''
    # actor = (i.text.strip() for i in soup.select('span[onmouseover^="hoverdiv"]')) if soup.select('span[onmouseover^="hoverdiv"]') else ''
    actor_text = ''
    for tex in actor:
        actor_text += '%s   ' % tex
    categories['演員'] = actor_text

    #构建Ajax的链接地址
    # 网址加入字典
    url = soup.select('link[hreflang="zh"]')[0]['href']
    categories['URL'] = url

    # 将磁力链接加入字典
    cili = _get_cili_url(pagetext)
    magnet_html = downloader.get_html(cili, Referer_url=url)
    magnet = _parser_magnet(magnet_html)
    categories['magnet'] = magnet


    #torrentname = _parser_torrentname(magnet_html)
    categories['coverimage'] = ''
    categories['torrentname'] = 'NULL'
    categories['torrenthash'] = ''

    return categories
