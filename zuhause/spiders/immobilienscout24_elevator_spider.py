#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from zuhause.items import Home
from scrapy.spiders import CrawlSpider
from datetime import date
from zuhause.utils.date_parser import parse_date
from zuhause.utils.geo import coord
from zuhause.utils.geo import address
import re

class Immobilienscout24Spider(CrawlSpider):
    name = 'immobilien-elevator'
    start_urls = ['https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/-/-/EURO--1100,00/-/-/-/-/-/-/-/true']

    def parse(self, response):
        sel = Selector(response)

        total_pages = int(sel.xpath("//div[@id='pageSelection']//select//option//text()").extract()[-1])
        url = "https://www.immobilienscout24.de/Suche/S-T/P-%d/Wohnung-Miete/Berlin/Berlin/-/-/-/EURO--1100,00/-/-/-/-/-/-/-/true"

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
        home['source'] = 'immobilienscout24-elevator'
        home['furnished'] = False
        home['title'] = self.to_str(sel.xpath("//h1[@id='expose-title']//text()"))
        home['source_id'] = re.match(r'.*expose/(\d+)', response.url).group(1)

        attributes = sel.xpath("//div[@class='criteriagroup criteria-group--two-columns']")
        home['rooms'] = self.to_float(attributes.xpath("//dl//dd[contains(@class, 'zimmer')]//text()"))
        home['available_at'] = parse_date(self.to_str(attributes.xpath("//dl//dd[contains(@class, 'bezugsfrei')]//text()")))
        home['rent_price'] = self.format_price(sel.xpath("//dd[contains(@class, 'gesamtmiete')]//text()"))
        home['updated_at'] = date.today().isoformat()
        home['geolocation'] = self.geo(self.to_str(sel.xpath("//div[@id='half-page-ad-stick-stopper']//script//text()")))
        home['address'] = address(home['geolocation'])


        try:
            home['allows_pets'] = self.format_allows_pets(self.to_str(attributes.xpath("//dl//dd[contains(@class, 'haustiere')]//text()")))
            home['min_time_to_stay'] = self.to_str(attributes.xpath("//dl//dd[contains(@class, 'mindestmietdauer')]//text()"))
            home['dimensions'] = self.to_str(attributes.xpath("//dl//dd[contains(@class, 'wohnflaeche')]//text()"))
        except:
            pass

        return home

    def geo(self, content):
        latitude = re.search(r'.*lat:\s+(.*?),', content).group(1)
        longitude = re.search(r'.*lng:\s+(.*?)\s+', content).group(1)

        return "%s,%s" % (latitude, longitude)

    def to_float(self, element):
        return float(element.extract()[0].strip().replace(",", "."))

    def to_str(self, element):
        return str(element.extract()[0].encode("utf-8")).strip()

    def format_price(self, element):
        return float(self.to_str(element).split()[0].replace(",", "").replace(".", ""))

    def format_allows_pets(self, content):
        if('Nein' in content):
            return 'no'

        return 'yes'
