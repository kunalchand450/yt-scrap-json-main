import os, tempfile, json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class AmazonspiderSpider(CrawlSpider):
    name = 'amazonspider'
    allowed_domains = ['amazon.in']
    # start_urls = ['https://www.amazon.in/s?k=printers&ref=nb_sb_noss']
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(
            "//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2' or @class='a-size-mini a-spacing-none a-color-base s-line-clamp-4' or @class='a-size-mini a-spacing-none a-color-base s-line-clamp-3' or @class='a-size-mini a-spacing-none a-color-base s-line-clamp-1' or @class='a-size-mini a-spacing-none a-color-base s-line-clamp-5' or @class='a-size-mini a-spacing-none a-color-base s-line-clamp-6']/a")), callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")),
    )
    with open(os.path.join(tempfile.gettempdir(),'start_urls.json')) as tempurlfilepointer:
        start_urls = json.loads(tempurlfilepointer.read())['urls']
        print(f'here be the start urls {start_urls}') #this code will take url from temp folder and insert in scrapy start url in default settings

    def parse_item(self, response):
        item = {}
        item['parent_url'] = response.request.headers['referer'].decode('utf-8')
        item['product_name'] = response.xpath(
            'normalize-space(//h1[@class="a-size-large a-spacing-none" or @class="a-size-large a-spacing-none"]/span/text())').get()
        item['price'] = response.xpath(
            "//span[@class='a-price a-text-price a-size-medium apexPriceToPay' or @class='a-price aok-align-center reinventPricePriceToPayMargin priceToPay']//span[1]/text()").get()
        item['description'] = response.xpath(
            "//ul[@class='a-unordered-list a-vertical a-spacing-mini']//span/text()").get()
        item['item_url'] = response.url

        return item
