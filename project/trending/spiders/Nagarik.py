import scrapy
from Utils import Utils
from Utils import PostNews

import logging
logging.getLogger().setLevel(logging.ERROR)
# Disable all logging messages (including Scrapy's) below WARNING level
logging.getLogger('scrapy').setLevel(logging.ERROR)
#news=[]

class Nagarik(scrapy.Spider):
    name="Nagarik"
    start_urls = ['https://nagarikpost.com/']
    scraped_items = []

    def __init__(self):
        self.article_xpath='//div[@class="maghny-grids-inf row mx-1"]/div'
        self.title_xpath='.//h2/a/text()'
        self.link_xpath='.//h2/a'
        self.main_section_xpath='//div[@class=" bg-white"]'
        self.img_src_xpath='.//div[@class=" description "]/img'
        self.description_xpath='.//div[@class="desc"]/p/text()'
        self.date_xpath='//p[@class="text-muted font-italic"]/text()'

    def parse(self, response):
        print('--------------------Scrapping Nagarik News------------------------------')
        for article in response.xpath(self.article_xpath):
            title=article.xpath(self.title_xpath).get()
            try:
                get_link=article.xpath(self.link_xpath).attrib['href']
            except Exception as e:
                print(e)

            yield scrapy.Request(url=get_link, callback=self.parse_article,meta={'title':title,'link':get_link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        img_src=main_section.xpath(self.img_src_xpath).attrib['src']
        description=response.xpath(self.description_xpath).getall()
        content_description = ''.join(description)
        content = Utils.word_60(content_description)
        date=main_section.xpath(self.date_xpath).get().strip()
        published_date = Utils.nagariknews__dateconverter(date)

        news = {
            'title':title,
            'content_description':content,
            'published_date':published_date,
            'image_url':img_src, 
            'url':response.meta['link'],
            'is_recent':True,
            'category_name':'others',
            'source_name':'nagariknews',
            'is_trending':True 
            }
        
        PostNews.postnews(news)

