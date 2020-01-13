# -*- coding: utf-8 -*-
import scrapy
from scrapy import *
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider

class ProvaSpider(CrawlSpider):
    name = 'prova'
    allowed_domains = ['stockx.com']
    start_urls = ['https://stockx.com/sneakers/release-date']

    def parse(self, response,):
        links = response.xpath(
            '//*[@id="products-container"]//div[@class="tile Tile-oazi1d-0 bbbEOC"]/a/@href').extract()
        for link in links:
            yield Request("https://stockx.com" + link, callback=self.parse_sneaker_link,dont_filter = True)
        page_link = response.xpath(
            "//*[@id=\"browse-wrapper\"]//a[@class=\"pointer NavButton__NavigationButton-hkt558-0 dyMfjb\"]/@href").extract()
        print (page_link)
        if response.xpath('//*[@id="products-container"]//div[@class="tile Tile-oazi1d-0 bbbEOC"]/a/text()').extract()==25:
            raise CloseSpider('fine')
        if len(page_link)>1:
            yield Request("https://stockx.com"+page_link[1],callback=self.parse,dont_filter = True)
        else:
            yield Request("https://stockx.com" + page_link[0], callback=self.parse, dont_filter=True)

    def parse_sneaker_link(self, response):
        info = {
            'nome' : response.xpath('//*[@id="product-header"]/div[1]/div/h1/text()').extract(),
            'style_code' : response.xpath('.//span[@data-testid="product-detail-style"]/text()').extract(),
            'colorway' : response.xpath('.//span[@data-testid="product-detail-colorway"]/text()').extract(),
            'retail_price': response.xpath('.//span[@data-testid="product-detail-retail price"]/text()').extract(),
            'realease_date':response.xpath('.//span[@data-testid="product-detail-release date"]/text()').extract()

        }
        yield info