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

class Immobilienscout24Spider(CrawlSpider):
    name = 'immobilien'
    start_urls = ['https://www.immobilienscout24.de/Suche/S-T/P-1/WAZ/Umkreissuche/Berlin_2dMitte_20_28Mitte_29/10178/228180/2512256/Alexanderplatz/-/100']

    def parse(self, response):
        sel = Selector(response)

        total_pages = int(sel.xpath("//div[@id='pageSelection']//select//option//text()").extract()[-1])
        url = "https://www.immobilienscout24.de/Suche/S-T/P-%d/WAZ/Umkreissuche/Berlin_2dMitte_20_28Mitte_29/10178/228180/2512256/Alexanderplatz/-/100"

        for x in range(1, total_pages + 1):
            yield Request(url % x, self.parse_search_results)

    def parse_search_results(self, response):
        sel = Selector(response)
        exposes = sel.xpath("//ul[@id='resultListItems']//li[@class='result-list__listing ']//@data-id").extract()

        for expose in exposes:
            url = "https://www.immobilienscout24.de/expose/%s" % str(expose)
            yield Request(url, self.parse_expose_data)

    def parse_expose_data(self, response):
        sel = Selector(response)
        home = Home()

        home['url'] = response.url
        home['source'] = 'immobilienscout24'
        home['furnished'] = True
        home['title'] = self.to_str(sel.xpath("//h1[@id='expose-title']//text()"))
        home['source_id'] = re.match(r'.*expose/(\d+)', response.url).group(1)

        attributes = sel.xpath("//div[@class='criteriagroup print-two-columns']")
        home['rooms'] = self.to_float(attributes.xpath("//dl//dd[contains(@class, 'zimmer')]//text()"))
        home['dimensions'] = self.to_str(attributes.xpath("//dl//dd[contains(@class, 'wohnflaeche')]//text()"))
        home['available_at'] = parse_date(self.to_str(attributes.xpath("//dl//dd[contains(@class, 'bezugsfrei')]//text()")))
        home['min_time_to_stay'] = self.to_str(attributes.xpath("//dl//dd[contains(@class, 'mindestmietdauer')]//text()"))
        home['rent_price'] = self.format_price(sel.xpath("//div[contains(@class, 'mietemonat')]//text()"))
        home['updated_at'] = date.today().isoformat()
        home['geolocation'] = self.geo(self.to_str(sel.xpath("//div[contains(@class, 'map-container')]//script//text()")))

        print(home)

    def geo(self, content):
        latitude = re.search(r'.*latitude\":\s+\"(.*)\",', content).group(1)
        longitude = re.search(r'.*longitude\":\s+\"(.*)\",', content).group(1)

        return "%s,%s" % (latitude, longitude)

    def to_float(self, element):
     return float(element.extract()[0].strip())

    def to_str(self, element):
     return str(element.extract()[0].encode("utf-8")).strip()

    def format_price(self, element):
     return self.to_str(element).split()[0].replace(",", "").replace(".", "")
