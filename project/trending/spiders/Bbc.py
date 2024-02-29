import scrapy
from Utils import PostNews
from Utils import Utils


import logging
logging.getLogger().setLevel(logging.ERROR)
# Disable all logging messages (including Scrapy's) below WARNING level
logging.getLogger('scrapy').setLevel(logging.ERROR)
#news=[]

class Bbc(scrapy.Spider):
    name="bbc"
    start_urls = ['https://www.bbc.com/nepali']
    scraped_items = []
    def __init__(self):
        self.articles_section_xpath="//div[@data-testid='hierarchical-grid']/ul"
        self.article_xpath='.//li'
        self.title_xpath='.//div/div[@class="promo-text"]/h3/a/text()'
        self.alternate_title_xpath='.//div/div[@class="promo-text"]/h3/a/span/text()'
        self.link_xpath='.//div/div[@class="promo-text"]/h3/a'
        self.main_section_xpath='//main'
        self.img_src_xpath='.//figure/div/picture/img/@src'
        self.alternate_img_src_xpath='.//div/div/figure/div/div/img/@src'
        self.description_xpath='.//div[@dir="ltr"]/p'
        self.date_xpath='.//div/time/@datetime'

    def parse(self, response):
        print('--------------------Scrapping BBC Nepali------------------------------')
        articles=response.xpath(self.articles_section_xpath)[0]
        count=0
        for article in articles.xpath(self.article_xpath):
            count+=1
            title=article.xpath(self.title_xpath).get()
            if title is None:
                title=article.xpath(self.alternate_title_xpath).get()
            link=article.xpath(self.link_xpath).attrib['href']
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        
        img_src=main_section.xpath(self.img_src_xpath).get()
        if img_src is None:
            img_src=main_section.xpath(self.alternate_img_src_xpath).get()
        description_elements=main_section.xpath(self.description_xpath)
        description=""
        for item in description_elements:
            description = description + item.xpath('.//text()').get()+"\n"
            if len(description.split())>60:
                description=description.strip()
                break
        content = Utils.word_60(description)
        date=main_section.xpath(self.date_xpath).get().strip()
        category='others'
        news = {
            'title':title,
            'content_description':content,
            'published_date':date,
            'image_url':img_src, 
            'url':link,
            'is_recent':True,
            'category_name':category,
            'source_name':'KathmanduPost',
            'is_trending':True 
            }
        
        PostNews.postnews(news)



 