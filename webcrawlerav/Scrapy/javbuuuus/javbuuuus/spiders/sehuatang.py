import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SehuatangSpider(CrawlSpider):
    name = 'sehuatang'
    allowed_domains = ['www.sehuatang.net']
    start_urls = ['https://www.sehuatang.net/forum-37-1.html']

    rules = (
        Rule(LinkExtractor(allow=r'forum-37-\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response, **kwargs):
        #print(response)
        #threadlinks = response.xpath("//table[@id='threadlisttableid']/tbody[contains(@id,'normalthread_')]//a[@class='s xst']").extract()
        #print(threadlinks)
        pass

    def parse_item(self, response):
        #620200-000016-0000

        #<tbody id="normalthread_518154">
        #<a href="thread-518154-1-1.html" onclick="if (!window.__cfRLUnblockHandlers) return false; atarget(this)" class="s xst">ply-007 元「ウルトラボディー大会」九州○○県第一位七尾みさき/天方ゆこ</a>
        #//tr[contains(@class,'result')]
        print(response)
        threadlinks = response.xpath("//table[@id='threadlisttableid']/tbody[contains(@id,'normalthread_')]//a[@class='s xst']")
        #print(threadlinks)
        for avthread in threadlinks:
            strtitle = avthread.xpath("text()").extract()
            avlink = avthread.xpath("@href").extract()

            if strtitle != None and avlink != None:
                avid = strtitle[0].split(" ", 1)
                print(avid[0],strtitle[0])
        #/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody[10]/tr/th/a[2]



        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
