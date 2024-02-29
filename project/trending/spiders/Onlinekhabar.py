import scrapy
from Utils import Utils
from Utils import PostNews

class onlinekhabar(scrapy.Spider):
    name = 'onlinekhabar'
    
    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.onlinekhabar.com/']
        self.data = []
        self.titlePath = '//div[@class="ok-post-title-right"]/h1/text()'
        self.imagepath = '//div[@class="post-thumbnail"]/img/@src'
        self.paragraphpath= '//div[@class="ok18-single-post-content-wrap"]/p/text()'
        self.datepath = '//div[@class="ok-post-title-right"]/div[@class="ok-title-info flx"]/div[@class="ok-news-post-hour"]/span/text()'

    def start_request(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)

    def parse(self, response):
        print('--------------------Scrapping Online khabar------------------------------')
        for links in response.xpath('//div[@class="span-5 "]/div'):
            link = links.css('a').attrib["href"]
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        title = response.xpath(self.titlePath).get()
        image = response.xpath(self.imagepath).get()
        paragraph = response.xpath(self.paragraphpath).getall()
        merged_paragraph = ''.join(paragraph)
        content = Utils.word_60(merged_paragraph)
        date = response.xpath(self.datepath).get()
        published_date = Utils.online_khabar_conversion(date)

        news = {
            "title":title,
            "content_description":content,
            "published_date":published_date,
            "image_url":image, 
            "url":response.meta['link'],
            "is_recent":True,
            "category_name":'others',
            "source_name":'onlinekhabar',
            "is_trending":True
            }
        
        PostNews.postnews(news)


