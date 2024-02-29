import scrapy
from Utils import PostNews
from Utils import Utils

class Annapurna(scrapy.Spider):
    name="annapurna"
    start_urls = ['https://www.annapurnapost.com/']

    def __init__(self):
        self.f_annapurna()

    def f_annapurna(self):
        self.article_xpath='//div[@class="breaking__news"]'
        self.title_xpath='.//h1/a/text()'
        self.link_xpath='.//h1/a'
        self.main_section_xpath='//div[@class="ap__news-content"]'
        self.img_src_xpath='//div[contains(@class,"img__withSound")]/figure/img/@src'
        self.description_xpath='//div[@class="news__details"]/p'
        self.date_xpath='//p[@class="date"]/span/text()'
        self.category ='//div[@class="card__category"]/a'

    def parse(self, response):
        print('--------------------Scrapping Annapurna Post------------------------------')
        for article in response.xpath(self.article_xpath):
            title=article.xpath(self.title_xpath).get().replace('\n','').strip()
            get_link=article.xpath(self.link_xpath).attrib['href']
            link=f"https://www.annapurnapost.com{get_link}"
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link})

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        main_section=response.xpath(self.main_section_xpath)
        #/div[contains(@class, 'description')]/div/figure/img/@data-src"
        img_src=main_section.xpath(self.img_src_xpath).get()
        desc=response.xpath(self.description_xpath)

        description=""
        for item in desc:
            description = description + item.xpath('.//text()').get()+"\n"
            if len(description.split())>60:
                description=description.strip()
                break
        
        content = Utils.word_60(description)

        # raw_date=main_section.xpath(self.date_xpath).get()
        # date = Utils.annapurnapost_datetime(raw_date)
        news = {
            'title':title,
            'content_description':content,
            'published_date':date,
            'image_url':img_src,
            'url':link,
            'category_name':'others',
            'is_recent':True,
            'source_name':'annapurnapost',
            'is_trending':True 
            }
        PostNews.postnews(news)
        


