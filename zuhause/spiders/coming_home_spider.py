#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from zuhause.items import Home
from scrapy.spiders import CrawlSpider
from datetime import date

class ComingHomeSpider(CrawlSpider):
    name = "coming_home"
    start_urls = ["http://en.coming-home.org/suche_3.php"]

    def parse(self, response):
        sel = Selector(response)
        total_pages = int(sel.xpath("//div[@class='sucheHeader']//div//strong//text()").extract()[2])

        for x in range(1, total_pages + 1):
            url = "http://en.coming-home.org/suche_3.php?pageNr=%d" % x
            yield Request(url, self.parse_search_results)

    def parse_search_results(self, response):
        sel = Selector(response)
        exposes = sel.xpath("//div[@class='suche_teaser_right']//p//a[@class='colorSuche']//@href").extract()

        for expose in exposes:
            url = "http://en.coming-home.org/%s" % str(expose)
            yield Request(url, self.parse_expose_data)

    def parse_expose_data(self, response):
        sel = Selector(response)
        home = Home()

        home["url"] = response.url
        home["site"] = "coming-home"
        home["furnished"] = True
        home["title"] = sel.xpath("//h2//text()").extract()[0]
        home["site_id"] = str(sel.xpath("//table//tr//th//text()").extract()[0]).strip().split("Offer no. ")[1]
        home["dimensions"] = sel.xpath("//table//tr//td//text()").extract()[0]
        home["available_at"] = str(sel.xpath("//table//tr//td//text()").extract()[1])
        home["min_time_to_stay"] = str(sel.xpath("//table//tr//td//text()").extract()[2]).split("min. ")[1]
        home["rent_price"] = float(sel.xpath("//table//tr//td//text()").extract()[3].encode("utf-8").split(",00\xc2")[0].replace(".", ""))
        home["deposit"] = sel.xpath("//table//tr//td//text()").extract()[5]
        home["location"] = sel.xpath("//table//tr//td//text()").extract()[8].strip()
        home["description"] = sel.xpath("//table//tr//td//text()").extract()[11]
        home["updated_at"] = date.today().isoformat()

        return home
