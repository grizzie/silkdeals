
    # def remove_characters(self, value):
    #     return value.strip('\n')

# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider
from shutil import which
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_path = which("chromedriver")

chrome_options = Options() #5
#6 chrome_options.add_argument("--headless") #5

#1 driver = webdriver.Chrome(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options) #2
driver.get("https://slickdeals.net/computer-deals")
class ComputerdealsSpider(CrawlSpider):
    name = 'computerdeals'
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class=\'itemImageLink\']/span/following-sibling::a'), callback='parse', follow=True),)

    # def start_requests(self):
    #     yield SeleniumRequest(
    #         url='https://slickdeals.net/computer-deals',
    #         wait_time=3,
    #         callback=self.parse
    #     )
 
    def parse(self, response):
        yield{
            'name':response.xpath("//div[@class='dealPrice']/@title").get()
                # 'name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                # 'link':response.urljoin(product.xpath(".//div[@class='itemImageLink']/a/@href").get()),
                # 'store_name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                # 'price':product.xpath(".//div[@class='itemPrice  wide ']/text()").get()
        }

        next_page = response.xpath("(//div[contains(@class,'pagination')]/a)[2]/@href").get()
        if next_page:
            absolute_url = f'https://slickdeals.net{next_page}'
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
