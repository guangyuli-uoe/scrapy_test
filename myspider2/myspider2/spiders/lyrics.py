import scrapy


class LyricsSpider(scrapy.Spider):
    name = 'lyrics'
    allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.xxx.com/']

    def parse(self, response):
        pass
