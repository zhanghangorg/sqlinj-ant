import scrapy

class BlogSpider(scrapy.Spider):
    name = 'youzuspider'
    start_urls = ['http://www.youzu.com']

    def parse(self, response):  
		hxs = HtmlXPathSelector(response)  
		items = []  
		
		newurls = hxs.select('//a/@href').extract()  
		validurls = []  
		    for url in newurls:  
		            #判断URL是否合法   
		            if true:  
		                    validurls.append(url)  
		
		    items.extend([self.make_requests_from_url(url).replace(callback=self.parse) for url in validurls])  
		
		    sites = hxs.select('//ul/li')  
		    items = []  
		    for site in sites:  
		            item = DmozItem()  
		            item['title'] = site.select('a/text()').extract()  
		            item['link'] = site.select('a/@href').extract()  
		            item['desc'] = site.select('text()').extract()  
		            items.append(item) 
