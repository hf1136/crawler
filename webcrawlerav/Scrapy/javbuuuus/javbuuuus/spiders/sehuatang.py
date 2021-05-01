import scrapy

from scrapy import Spider

from javbuuuus.items import SehuatangItem


class SehuatangSpider(Spider):
    name = 'sehuatang'
    allowed_domains = ['www.sehuatang.net']
    start_urls = ['https://www.sehuatang.net/forum-37-1.html']
    domain = 'https://www.sehuatang.net/'
    pagenumber = 1
    maxpage = 10

    def parse(self, response):
        print(response)
        threadlinks = response.xpath("//table[@id='threadlisttableid']/tbody[contains(@id,'normalthread_')]//a[@class='s xst']")
        for avthread in threadlinks:
            strtitle = avthread.xpath("text()").extract()
            avlink = avthread.xpath("@href")[0].extract()

            if strtitle != None and avlink != None:
                avid = strtitle[0].split(" ", 1)
                print(avid[0],strtitle[0],avlink)
                yield scrapy.Request(self.domain + avlink, callback=self.parse_detail)

        self.pagenumber += 1
        nextpagelink = f'forum-37-{self.pagenumber}.html'

        if self.pagenumber < self.maxpage:
            yield scrapy.Request(self.domain + nextpagelink,callback=self.parse)

    def parse_detail(self,r):
        print(r)
        categories = {}

        categories['URL'] = r.url
        categories['coverimage'] = ''
        categories['detail'] = ''
        categories['magnetuploadtime'] = ''

        magnet = r.xpath(".//ol/li/text()")[0].extract()
        categories['magnet'] = magnet

        linerow1 = r.xpath(".//p[@class='xg1 y']/span/@title")[0].extract()


        if (linerow1):
            categories['magnetuploadtime'] = linerow1

        linerow = r.xpath('.//td[@class="t_f"]/text()').extract()
        i = 0
        for lil in linerow:
            rowt = str(lil)
            categories['detail'] += rowt.replace('       ', '')
            if i == 12:
                break
            i += 1

        img1 = r.xpath(".//img[contains(@id ,'aimg')]/@file")[0].extract()
        img2 = r.xpath(".//img[contains(@id ,'aimg')]/@file")[1].extract()

        categories['coverimage'] = img1 + "||" + img2

        #<span id="thread_subject">484TIGER-002 永瀬ゆい 帰ってきた！カリスマAV監督タイガ</span>
        strtitle = r.xpath(".//span[@id='thread_subject']/text()")[0].extract()



        categories['title'] = strtitle.split(" ")[1]
        categories['avid'] = strtitle.split(" ")[0]

        item = SehuatangItem()
        item['avid'] = categories['avid']
        item['title'] = categories['title']
        item['coverimage'] = categories['coverimage']
        item['detail'] = categories['detail']
        item['magnetuploadtime'] = categories['magnetuploadtime']
        item['magnets'] = categories['magnet']

        print(item)
        yield item