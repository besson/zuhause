#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from zuhause.items import Home
from scrapy.spiders import CrawlSpider
from datetime import date
from zuhause.utils.date_parser import parse_date
from zuhause.utils.geo import coord
import re

class ComingHomeSpider(CrawlSpider):
    name = 'coming-home'
    start_urls = ['http://en.coming-home.org/suche_3.php']

    def parse(self, response):
        sel = Selector(response)
        total_pages = int(sel.xpath('//div[@class="sucheHeader"]//div//strong//text()').extract()[2])

        for x in range(1, total_pages + 1):
            url = 'http://en.coming-home.org/suche_3.php?pageNr=%d' % x
            yield Request(url, self.parse_search_results)

    def parse_search_results(self, response):
        sel = Selector(response)
        exposes = sel.xpath('//div[@class="suche_teaser_right"]//p//a[@class="colorSuche"]//@href').extract()

        for expose in exposes:
            url = 'http://en.coming-home.org/%s' % str(expose)
            yield Request(url, self.parse_expose_data)

    def parse_expose_data(self, response):
        sel = Selector(response)
        home = Home()

        home['url'] = response.url
        home['source'] = 'coming-home'
        home['furnished'] = True
        home['title'] = sel.xpath('//h2//text()').extract()[0]
        home['source_id'] = str(sel.xpath('//table//tr//th//text()').extract()[0]).strip().split('Offer no. ')[1]
        home['dimensions'] = sel.xpath('//table//tr//td//text()').extract()[0]
        home['available_at'] = parse_date(str(sel.xpath('//table//tr//td//text()').extract()[1]))
        home['min_time_to_stay'] = str(sel.xpath('//table//tr//td//text()').extract()[2]).split('min. ')[1]
        home['rent_price'] = float(sel.xpath('//table//tr//td//text()').extract()[3].encode('utf-8').split(',00\xc2')[0].replace('.', ''))
        home['deposit'] = sel.xpath('//table//tr//td//text()').extract()[5]
        home['location'] = sel.xpath('//table//tr//td//text()').extract()[8].strip()
        home['description'] = ' '.join([x.strip() for x in sel.xpath('//table//tr//td//text()').extract()])
        home['updated_at'] = date.today().isoformat()
        home['address'] = self.address(response.body)
        home['geolocation'] = coord(home['address'])
        home['allows_pets'] = self.format_allows_pets(home['description'])

        return home

    def address(self, body):
        match = re.search( r'geocoder\.getLatLng\(\s*\'(.*)\',\n\t\t', body)

        if (match):
            return str(match.group(1))
        else:
            return ''

    def format_allows_pets(self, content):
        if('pets not allowed' in content):
            return 'no'

        return 'yes'
