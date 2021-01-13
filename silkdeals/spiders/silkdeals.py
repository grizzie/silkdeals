
    # def remove_characters(self, value):
    #     return value.strip('\n')

# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
 
class ComputerdealsSpider(scrapy.Spider):
    # name = 'computerdeals'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals',
            wait_time=3,
            callback=self.parse
        )
    
    

    def parse(self, response):
        products = response.xpath("//li[contains(@class,'fpGridBox grid')]")
        for product in products:
            yield{
                'name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                'link':response.urljoin(product.xpath(".//div[@class='itemImageLink']/a/@href").get()),
                'store_name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                'price':product.xpath(".//div[@class='itemPrice  wide ']/text()").get()
            }
 
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f'https://slickdeals.net{next_page}'
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
