from typing import Any
import scrapy
from Utils import Utils
from Utils import PostNews

class Ratopati(scrapy.Spider):
    name = 'Ratopati'

    def __init__(self, name: str | None = None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.ratopati.com/']
        self.data = []
        self.titlePath = '//div/h2[@class = "heading"]/text()'
        self.imagepath = '//figure[@class = "featured-image"]/img/@src'
        self.paragraphpath= '//div[@class = "the-content"]/p/text()'
        self.datepath = '//div/span[@class="date"]/text()'

    def start_request(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        print('--------------------Scrapping Rato Pati------------------------------')
        for div in response.css('.heading.text--black'): #main div css 
            link = div.css('a').attrib["href"] 
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        header = response.xpath(self.titlePath).get() 
        title = header.strip()
        image = response.xpath(self.imagepath).get()
        paragraph = response.xpath(self.paragraphpath).getall()
        merged_paragraph = ''.join(paragraph)
        content = Utils.word_60(merged_paragraph)
        date = response.xpath(self.datepath).get()
        published_date = Utils.ratopati_date_conversion(date)

        news = {
            'title':title,
            'content_description':content,
            'published_date':published_date,
            'image_url':image, 
            'url':response.meta['link'],
            'is_recent':True,
            'category_name':'others',
            'source_name':'ratopatinepali',
            'is_trending':True 
            }
        PostNews.postnews(news)
  