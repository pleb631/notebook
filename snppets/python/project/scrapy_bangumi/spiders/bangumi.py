import scrapy
import pprint
from scrapy_learn.items import ScrapyBangumiItem


class BangumiSpider(scrapy.Spider):
    name = "bangumi"
    allowed_domains = ["bangumi.tv"]
    start_urls = ["https://bangumi.tv/anime/browser/?sort=rank&page=1"]
    base_url = "https://bangumi.tv/anime/browser/?sort=rank&page="
    page = 1
    def parse(self, response):
        data = response.xpath("//ul[@id='browserItemList']/li")
        for item in data:
            chName = item.xpath(".//div/h3/a/text()").extract_first()
            href = item.xpath(".//div/h3/a/@href").extract_first()
            oriName = item.xpath(".//div/h3/small/text()").extract_first()
            info = item.xpath(".//div/p[@class='info tip']/text()").extract_first().strip()
            imgUrl = item.xpath('.//a/span[@class="image"]/img/@src').extract_first()
            bangumiItem = ScrapyBangumiItem(chName=chName, oriName=oriName, info=info,href=href,imgUrl=imgUrl)
            
            yield bangumiItem
            
        
        if self.page<5:
            self.page+=1
            url = self.base_url+str(self.page)
            yield scrapy.Request(url=url,callback=self.parse)