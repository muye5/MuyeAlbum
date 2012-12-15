#coding=utf-8
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from crawl.items import CrawlItem
from crawl.items import URLItem
import URLFilter

num = 10
cnt = 0
urlbf = URLFilter.URLBloomFilter()
urlbf.initdb()
urlbf.initfilter()
urlbf.initclear('adds')
urlbf.initsql(m_sql = 'insert into adds (url) values(%s)')

class DmozSpider(BaseSpider):
    name = "sina_image"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
           "http://slide.eladies.sina.com.cn/"
    ]

    def parse(self, response):
        global num
        global cnt
        if num <= cnt:
            return
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//td/a')
        items = []
        for site in sites:
            url = site.select('./@href').extract()[0]
            item = Request(url, callback = self.crawlpicture)
            items.append(item)
        nexturl = hxs.select('//div[contains(@class, "page")]/a/@href').extract()[-2]
        base = get_base_url(response)
        nexturl = urljoin_rfc(base, nexturl)
#        print "*********", nexturl, "*********"
        items.append(Request(nexturl, callback = self.parse))
        return items

    def crawlpicture(self, response):
        global num
        global cnt
        global urlbf

        if num <= cnt:
            return
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//dl/dd[1]')
        items = []
        for site in sites:
            relative_url = site.select('./text()').extract()
            item = CrawlItem()
            tmp = []
            for ru in relative_url:
                if urlbf.add(ru):
                    tmp.append(ru)
                    cnt = cnt + 1
                    if num <= cnt:
                        break
            item['image_urls'] = tmp[0:]
            items.append(item)
            if num <= cnt:
                break
        return items

