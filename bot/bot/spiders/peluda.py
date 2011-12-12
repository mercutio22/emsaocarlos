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
		itineraries = dictionary of the type pk: (busline, departure, arrival).
		pk stands for primary key. 
		(Surprisingly busline numbers are not unique thus can't be used)
		Uses parse_item as callback for each weblink containing busline 
		routes and yields the respective LinhaItems.
		"""
		
		hxs = HtmlXPathSelector(response)
		itineraries = {}
		
		buslines = hxs.select('//td[contains(@width, "56")]')
		buslines = buslines.select('./p/b/span/text()').extract()
		buslinefilter = re.compile('\d\d\d\d')
		buslines = filter(buslinefilter.search, buslines)
					
		departures = hxs.select('//td[contains(@width, "52")]')
		departures = departures.select('./p/span/text()').extract()
		timefilter =  re.compile('\d\d:\d\d', re.IGNORECASE)
		departures = filter(timefilter.search, departures)
		departures.append('-') #the last 5871 busline has an undefined departure time!

		arrivals = hxs.select('//td[contains(@width, "50")]')
		arrivals = arrivals.select('./p/span/text()').extract()
		arrivals = filter(timefilter.search, arrivals)
		
		assert len(arrivals) == len(departures) == len(buslines), "Not the same ammount of buslines, departures or arrivals"

	    index = 0
	    while index < len(arrivals):
			intineraries[counter] = (index,
									busline[index],
									departures[index],
									arrivals[index])
									
		
		
		
		
	    
	    
	    
	    
	    
	   

	   
	   
	   
	   
		
		
				
		
			
		 
		
		
		
		
		
