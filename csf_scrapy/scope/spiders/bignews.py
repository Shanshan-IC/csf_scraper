# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Selector
import scrapy
from scrapy.loader import ItemLoader
from scope.items import NewsItem
from datetime import datetime
import os
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
import time


class BigNewsSpider(Spider):
    name = "bignews"
    allowed_domains = ["bignews.la"]
    start_urls = ["http://www.bignews.la/newslist.html"]

    interval = 60 * 5

    def __init__(self, txt_path=None, *args, **kwargs):
        Spider.__init__(self, *args, **kwargs)

        if not txt_path:
            txt_path = "%s%s%s" % (os.curdir, os.sep, self.name)

        if not os.path.exists(txt_path):
            os.mkdir(txt_path)

        self.txt_path = txt_path

        dispatcher.connect(self.spider_idle, signals.spider_idle)

    def spider_idle(self, spider):
        for req in self.start_requests():
            self.crawler.engine.crawl(req, spider)

        time.sleep(self.interval)

    def parse(self, response):
        for li in response.css(".menu li"):
            one_n = li.css("::attr(id)").extract_first()
            cate = li.css("::text").extract_first()
            url_id = "con_" + one_n[:3] + "_" + one_n[3:]

            request = scrapy.Request(
                response.css("#%s > iframe::attr(src)" % url_id).extract_first(),
                self.parse_cate,
                dont_filter=True)

            request.meta["cate"] = cate
            yield request

    def parse_cate(self, response):
        for a in response.css("a::attr(onclick)"):
            lnk = a.re("openwin\('(.+)'\)")[0]

            request = scrapy.Request("http://news.bignews.la/%s" % lnk.strip(), self.parse_detail)
            request.meta["cate"] = response.meta["cate"]
            yield request

    def format_date(self, date):
        return "".join([s for s in date if s not in [" ", "-", ":"]]) \
               + "".join(["0" for i in range(0, 14 - len(date))])

    def parse_detail(self, response):
        item = NewsItem()
        item["url"] = response.url
        item["date"] = self.format_date(response.css("p > span::text").re("[0-9]{4}-[0-9]{2}-[0-9]{2}[0-9: ]*")[0])

        item["src"] = self.name
        src_lst = response.css("p > span::text").re(u"来源：(.+)")
        if src_lst:
            item["src"] = src_lst[0].strip()

        item["cate"] = response.meta["cate"]
        item["title"] = response.css("div > span *::text").extract_first()
        item["content"] = [
            c.replace("\r", "").replace("\n", "")
            for c in response.css("span > p *::text").extract()
            if c.strip() and c.strip() != u"内容："]

        item["ctime"] = datetime.now().strftime("%Y%m%d%H%M%S")

        yield item


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    cp = CrawlerProcess()
    cp.crawl(BigNewsSpider)
    cp.start()
