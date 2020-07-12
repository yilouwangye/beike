# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,Spider
from beike.items import BeikeItem
import re

class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['sz.zu.ke.com/zufang']
    start_urls = ['http://sz.zu.ke.com/zufang/']
    url = 'https://sz.zu.ke.com/zufang/luohuqu/pg2/#contentList'

    def start_requests(self):
        zone = ['luohuqu', 'futianqu', 'nanshanqu', 'yantianqu', 'baoanqu', 'longgangqu', 'longhuaqu', 'guangmingqu',
                'pingshanqu', 'dapengxinqu']
        # zone = ['futianqu','nanshanqu']
        base_url = 'https://sz.zu.ke.com/zufang/'
        for i in zone:
            for j in range(1,self.settings.get('MAX_PAGE')+1):
                url = base_url + i + '/pg' + str(j) + '/#contentList'
                yield Request(url=url,callback=self.parse)

    def parse(self, response):
        infos = response.css('.content__list--item')
        for info in infos:
            item = BeikeItem()
            item['zone'] = info.xpath('.//p[@class="content__list--item--des"]/a[1]/text()').extract_first(default='null')
            item['village'] = info.xpath('.//p[@class="content__list--item--des"]/a[2]/text()').extract_first(default='null')
            item['house'] = info.xpath('.//p[@class="content__list--item--des"]/a[3]/text()').extract_first(default='null')
            item['sale'] = info.xpath('.//p[@class="content__list--item--des"]/span[@class="room__left"]/text()').extract_first('null')
            item['area'] = info.css('.content__list--item--des::text').extract()[4].strip().replace(' ', '') if len(info.css('.content__list--item--des::text').extract()) == 8 else info.css('.content__list--item--des::text').extract()[2].strip().replace(' ', '')
            item['position'] = info.css('.content__list--item--des::text').extract()[5].replace(' ', '') if len(info.css('.content__list--item--des::text').extract()) == 8 else info.css('.content__list--item--des::text').extract()[3].replace(' ','')
            item['layout'] = info.css('.content__list--item--des::text').extract()[6].strip().replace(' ','') if len(info.css('.content__list--item--des::text').extract()) == 8 else info.css('.content__list--item--des::text').extract()[4].strip().replace(' ','')
            item['style'] = info.css('.content__list--item--title a::text').extract_first().strip().replace(' ','').split('·')[0]
            item['price'] = info.css('.content__list--item-price em::text').extract_first() + info.css('.content__list--item-price::text').extract_first()
            item['tags'] = '/'.join(info.css('.content__list--item--bottom i::text').extract())
            item['description'] = 'https://sz.zu.ke.com/' + info.css('.content__list--item--title a::attr(href)').extract_first()
            yield item
            # self.logger.debug(item)
# scrapy crawl zufang


