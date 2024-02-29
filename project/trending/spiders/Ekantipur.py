import scrapy
from Utils import Utils
from Utils import PostNews

class Ekantipur(scrapy.Spider):    
    name = "ekantipur"
    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.start_urls = ['https://www.ekantipur.com/']
        self.titlePath = '//div[@class="article-header"]/h1/text()'
        self.imagepath = "//div[contains(@class, 'description')]/div/figure/img/@data-src"
        self.paragraphpath= '//div[@class="description current-news-block"]/p/text()'
        self.datepath = '//div[@class="time-author"]/time/text()'
       
    def start_request(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)

    def parse(self, response):
        print('-------Scraping Ekantipur')
        for links in response.xpath('//section[@class="main-news layout1"]/div/article/h2'): #main div
            link = links.css('a').attrib["href"]
            if link:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link})

    def parse_link(self, response):
        title = response.xpath(self.titlePath).get()
        image = response.xpath(self.imagepath).get()
        paragraph = response.xpath(self.paragraphpath).getall()
        content = ''.join(paragraph)
        description = Utils.word_60(content)
        date = response.xpath(self.datepath).get()
        if date == None:
            date = response.xpath('//div[@class="col-xs-12 col-sm-12 col-md-12"]/time/text()').get()
        published_date = Utils.ekantipur_conversion(date)
        category ="others"

        news = {
            'title':title,
            'content_description':description,
            'published_date':published_date,
            'image_url':image, 
            'url':response.meta['link'],
            'is_recent':True,
            'category_name':category,
            'source_name':'ekantipur',
            'is_trending':True 
            }
        
        PostNews.postnews(news)
