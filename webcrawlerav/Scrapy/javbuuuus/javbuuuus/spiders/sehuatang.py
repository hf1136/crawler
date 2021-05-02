import scrapy

from scrapy import Spider

from javbuuuus.items import SehuatangItem
from scrapy.utils.project import get_project_settings
import sqlite3

class SehuatangSpider(Spider):
    name = 'sehuatang'
    allowed_domains = ['www.sehuatang.net']
    start_urls = ['https://www.sehuatang.net/forum-37-1.html']
    domain = 'https://www.sehuatang.net/'
    pagenumber = 20
    maxpage = 50

    def parse(self, response):
        print(response)
        threadlinks = response.xpath("//table[@id='threadlisttableid']/tbody[contains(@id,'normalthread_')]//a[@class='s xst']")
        for avthread in threadlinks:
            strtitle = avthread.xpath("text()").extract()
            avlink = avthread.xpath("@href").extract_first()

            if strtitle != None and avlink != None:
                avid = strtitle[0].split(" ", 1)
                print(avid[0],strtitle[0],avlink)
                if self.check_url_not_in_table(self.domain + avlink):
                    yield scrapy.Request(self.domain + avlink, callback=self.parse_detail)

        self.pagenumber += 1
        nextpagelink = f'forum-37-{self.pagenumber}.html'

        if self.pagenumber < self.maxpage:
            yield scrapy.Request(self.domain + nextpagelink,callback=self.parse)

    def check_url_not_in_table(self, avlink):
        """check_url_in_db(url),if the url isn't in the table it will return True, otherwise return False"""
        settings = get_project_settings()
        conn = sqlite3.connect(settings["SQLITE_PATH"] + settings["SQLITE_DBNAME"])
        cursor = conn.cursor()

        cursor.execute('select URL from SHT_DATA where URL=?', (avlink,))
        check = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(check) > 0 :
            return False

        return True

    def parse_detail(self, r):
        categories = {}
        categories['URL'] = r.url
        categories['coverimage'] = ''
        categories['detail'] = ''
        categories['magnetuploadtime'] = ''

        magnet = r.xpath(".//ol/li/text()").extract_first()
        categories['magnet'] = ""
        if magnet != None:
            categories['magnet'] = magnet

        linerow1 = r.xpath(".//p[@class='xg1 y']/span/@title").extract()
        linerow2 = r.xpath(".//p[@class='xg1 y']/text()").extract()

        if (linerow1):
            categories['magnetuploadtime'] = linerow1[0]
        elif (linerow2):
            categories['magnetuploadtime'] = linerow2[0]

        linerow = r.xpath('.//td[@class="t_f"]/text()').extract()
        i = 0
        for lil in linerow:
            rowt = str(lil)
            categories['detail'] += rowt.replace('       ', '')
            if i == 12:
                break
            i += 1
        #src = "//cdn.jsdelivr.net/gh/stetoobpncg/weqsa//static/image/common/none.gif
        imgs = r.xpath(".//img[@src='//cdn.jsdelivr.net/gh/stetoobpncg/weqsa//static/image/common/none.gif']/@file").extract()
        for img in imgs:
            categories['coverimage'] = img + "||"

        #<span id="thread_subject">484TIGER-002 永瀬ゆい 帰ってきた！カリスマAV監督タイガ</span>
        strtitle = r.xpath(".//span[@id='thread_subject']/text()").extract_first()

        categories['title'] = ''
        categories['avid'] = ''

        if strtitle != None:
            categories['title'] = strtitle.split(" ")[1]
            categories['avid'] = strtitle.split(" ")[0]

        item = SehuatangItem()
        item['avid'] = categories['avid']
        item['title'] = categories['title']
        item['avurl'] = categories['URL']
        item['coverimage'] = categories['coverimage']
        item['detail'] = categories['detail']
        item['magnetuploadtime'] = categories['magnetuploadtime']
        item['magnets'] = categories['magnet']

        yield item