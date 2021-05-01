import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from  javbuuuus.items import MovieItem

import re
import math
import random
from pymongo import MongoClient

class JavbusallSpider(CrawlSpider):
    domain = 'www.javbus.com'
    name = 'javbusall'
    #allowed_domains = [domain]
    #start_urls = ['https://www.javbus.com/uncensored']
    start_urls = ['https://www.javbus.com']

    link = LinkExtractor(allow=r'page/\d+',deny=(r'/en/?|/ko/?|/ja/?|/uncensored|/genre|/actresses'))
    rules = (
        Rule(link, callback="parse_main",follow=False),
    )

    def parse_main(self, response):
        print(response)
        deatilpages = response.xpath("//a[@class='movie-box']/@href").extract()

        for moviedetailurl in deatilpages:

            strcode = moviedetailurl.replace('https://www.javbus.com/','')

            if not self.movieisintable(strcode):
                print(strcode)
                yield scrapy.Request(moviedetailurl,callback=self.parse_detial)

    def movieisintable(self,avcode):
        client = MongoClient("mongodb://127.0.0.1:27017/")
        database = client["JavBus"]
        collection = database["movie"]

        # Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/
        query = {}

        query["code"] = f"{avcode}"

        cursor = collection.find_one(query)
        try:
            if cursor is None:
                return False
        finally:
            client.close()
        return True

    def parse_detial(self, r):
        print('电影详情页: ' + r.url)
        title = cover = censored = censored = code = release_date = duration = \
            stars = previews = gid = uc = None
        director = {}
        studio = {}
        label = {}
        series = {}
        title = r.css('.col-md-9.screencap  img::attr(title)').extract_first()
        cover = r.css('.col-md-9.screencap  img::attr(src)').extract_first()
        censored = r.css('li.active > a::text').extract_first()
        tags = []
        for t in r.css('.genre  a[href*="genre"]'):
            tag = {
                'name': t.xpath('string(.)').extract_first(),
                'code': t.css('a::attr(href)').extract_first().split('/')[-1]
            }
            tags.append(tag)
        stars = []
        # stars = r.css('span[onmouseover] a::text').extract()
        for x in r.css('span[onmouseover] a'):
            star = {
                'name': x.xpath('string(.)').extract_first(),
                'code': x.xpath('.//@href').extract_first().split('/')[-1]
            }
            stars.append(star)
        previews = r.css('a.sample-box::attr(href)').extract()
        script = r.xpath('//script')[8].extract()
        for line in script.split('\n'):
            if 'gid' in line:
                gid = line.split('=')[-1].strip()[:-1]
            elif 'uc' in line:
                uc = line.split('=')[-1].strip()[:-1]
        magnets_url = 'https://' + self.domain + '/ajax/uncledatoolsbyajax.php?gid=' + gid + '&uc=' + uc + '&lang=en'
        for info in r.css('.info p'):
            header = info.css('.header::text').extract_first()
            other_code = None
            if header:
                data = info.xpath('string(.)').extract_first().replace(header, "").strip()
                if header == '導演:' or header == '製作商:' or header == '發行商:' or header == '系列:':
                    other_code = info.css('a::attr(href)').extract_first().split('/')[-1]

            if header == '識別碼:':
                code = data
            elif header == '發行日期:':
                release_date = data
            elif header == '長度:':
                duration = data
            elif header == '導演:':
                director['name'] = data
                director['code'] = other_code
            elif header == '製作商:':
                studio['name'] = data
                studio['code'] = other_code
            elif header == '發行商:':
                label['name'] = data
                label['code'] = other_code
            elif header == '系列:':
                series['name'] = data
                series['code'] = other_code
            elif header == '類別:' or header == '演員':
                pass
            elif header is None:
                pass
            else:
                print("存在未知字段!!!" + header)

        print(code)
        print(title)



        item = MovieItem()
        item['code'] = code
        item['title'] = title
        item['censored'] = censored
        item['stars'] = stars
        item['release_date'] = release_date
        item['duration'] = duration
        item['director'] = director
        item['studio'] = studio
        item['label'] = label
        item['tags'] = tags
        item['cover'] = cover
        item['previews'] = previews
        item['series'] = series
        item['magnets'] = None
        item['release_date'] = release_date
        magnets_url2 = self._get_cili_url(r.text)
        print(magnets_url2)
        yield scrapy.Request(magnets_url2, meta={'item': item}, callback=self.parse_magnets)

    def _get_cili_url(self,htmltext):
        """get_cili(soup).get the ajax url and Referer url of request"""

        pattern7 = re.compile("var gid = (\d+)", re.S)
        matcher7 = pattern7.search(htmltext)
        pattern8 = re.compile("img = '(.*?)'", re.S)
        matcher8 = pattern8.search(htmltext)

        ajax_get_cili_url = ''
        if matcher7:
            gid = matcher7.group(1)
            img = matcher8.group(1)
            ajax_get_cili_url = "https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid={}&lang=zh&img={}&uc=0&floor={}".format(
                gid,
                img,
                math.floor(random.random() * 1000 + 1))
        return ajax_get_cili_url

    def parse_magnets(self, r):
        item = r.meta['item']
        magnets = []
        for line in r.css('tr'):
            magnet = {}
            infos = line.css('a')
            if len(infos) == 5:
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[20:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = infos[1].xpath('string(.)').extract_first().strip() == 'HD'
                magnet['SUB'] = infos[2].xpath('string(.)').extract_first().strip() == 'SUB'
                magnet['magnet_size'] = infos[3].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[4].xpath('string(.)').extract_first().strip()
                magnets.append(magnet)
            elif len(infos) == 4:
                # 过滤magnet_url多余的后缀
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[20:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = infos[1].xpath('string(.)').extract_first().strip() == 'HD'
                magnet['SUB'] = infos[1].xpath('string(.)').extract_first().strip() == 'SUB'
                magnet['magnet_size'] = infos[2].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[3].xpath('string(.)').extract_first().strip()
                magnets.append(magnet)
            elif len(infos) == 3:
                # 过滤magnet_url多余的后缀
                magnet['magnet_url'] = infos[0].css('::attr(href)').extract_first().strip()[20:60]
                magnet['magnet_name'] = infos[0].xpath('string(.)').extract_first().strip()
                magnet['HD'] = False
                magnet['SUB'] = False
                magnet['magnet_size'] = infos[1].xpath('string(.)').extract_first().strip()
                magnet['magnet_date'] = infos[2].xpath('string(.)').extract_first().strip()
                magnets.append(magnet)
        item['magnets'] = magnets
        yield item