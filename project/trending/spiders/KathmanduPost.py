import scrapy
from datetime import datetime
from Utils import Utils
from Utils import PostNews

class KathmanduPost(scrapy.Spider):
    name="kathmandu_post"
    start_urls = ['https://kathmandupost.com']

    def __init__(self):
        self.news = []
        self.main_div_xpath='//div[@class="col-xs-12 col-sm-6 col-md-4 grid-first divider-right order-2--sm"]'
        self.article_xpath='.//article[contains(@class, "article-image article-image--left")]'
        self.title_xpath='//h1[@style]/text()'
        self.link_xpath='.//a'
        self.main_section_xpath='//div[@class="col-sm-8"]'
        self.img_src_xpath='//div[contains(@class,"row")]/div/img/@data-src'
        self.description_xpath='//section[@class="story-section"]/text()'
        self.date_xpath='//div[@class="updated-time"]/text()'

    def parse(self, response):
        print('--------------------Scrapping Kathmandu Post------------------------------')
        main_div = response.xpath(self.main_div_xpath)
        articles = main_div.xpath(self.article_xpath)

        for article in articles:
            link = article.xpath(self.link_xpath).attrib['href']
            yield scrapy.Request(url = self.start_urls[0] + link, callback = self.parse_article)


    def parse_article(self, response):
        print(f"visiting link {response.url}")
        article = response.xpath(self.main_section_xpath)
        title = article.xpath(self.title_xpath).get().strip()
        article_date = article.xpath(self.date_xpath).get()
        published_date_str = article_date.split(':', 1)[-1].strip()
        date = Utils.kathmandupost_conversion(published_date_str)

        try:
            date_object = datetime.strptime(published_date_str, '%B %d, %Y')
            formatted_date = date_object.strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")

        desc=response.xpath(self.description_xpath).getall()
        description = ''.join(desc)
        content = Utils.word_60(description)
        img_src = response.xpath(self.img_src_xpath).get()
        category = 'others'
        news = {
            'title':title,
            'content_description':content,
            'published_date':date,
            'image_url':img_src, 
            'url':response.url,
            'category_name':category,
            'is_recent':True,
            'source_name':'KathmanduPost',
            'is_trending':True 
            }
        PostNews.postnews(news)

    

