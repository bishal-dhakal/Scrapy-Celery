import scrapy
from Utils import Utils
from Utils import PostNews

class gorkhapatra(scrapy.Spider):
    name="gorkhapatra"
    start_urls = ['https://gorkhapatraonline.com/']
    def __init__(self):
        self.main_div_xpath='//div[@class="row"]'
        self.article_xpath='//div[@class="col-lg-12 mb-4"]'
        self.title_xpath='.//h2/a/text()'
        self.link_xpath='.//h2/a'
        self.main_section_xpath='//div[@class="col-lg-12"]'
        self.img_src_xpath='.//div[@class="blog-banner"]/img'
        self.description_xpath='//div[@class="blog-details"]/p'
        self.date_xpath='//span[@class="mr-3 font-size-16"]'

    def parse(self, response):
        print('--------------------Scrapping Gorkha Patra------------------------------')
        main_div=response.xpath(self.main_div_xpath)[2]
        for article in main_div.xpath(self.article_xpath):
            title=article.xpath(self.title_xpath).get().replace('\n','').strip()
            link=article.xpath(self.link_xpath).attrib['href']
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        img_src=response.xpath(self.img_src_xpath).attrib['src']
        desc=response.xpath(self.description_xpath).xpath('string()').getall()
        description = ''.join(desc)
        content = Utils.word_60(description)
        date=response.xpath(self.date_xpath)[0].xpath('string()').get().strip()
        published_date = Utils.gorkhapatraonline_datetime_parser(date)
        
        news = {
            'title':title,
            'content_description':content,
            'published_date':published_date,
            'image_url':img_src, 
            'url':link,
            'is_recent':True,
            'category_name':'others',
            'source_name':'gorkhapatra',
            'is_trending':True 
            }
            
        PostNews.postnews(news)
