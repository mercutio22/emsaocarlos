import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from bot.items import LinhaItem

class PeludaSpider(CrawlSpider):
    name = 'peluda'
    allowed_domains = ['www.athenaspaulista.com.br']
    start_urls = ['http://www.athenaspaulista.com.br/LINHAS/Linhas.htm']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Linha(\d+)'),
        callback='parse_mainpage', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = LinhaItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i


	def parse_mainpage(self, response):
		""" Parses the website containing the  itineraries
		itineraries = dictionary of the type busline: (departure, arrival)
		"""
		
		hxs = HtmlXPathSelector(response)
		itineraries = {}
		
		buslines = hxs.select('//td[contains(width, "56")]')
		buslines = buslines.select('./p/b/span/text()').extract()
		for i in buslines:
			
		 
		
		
		
		
		
