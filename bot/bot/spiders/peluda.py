import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from bot.items import LinhaItem
from scrapy.http import Request


class PeludaSpider(CrawlSpider):
    name = 'peluda'
    allowed_domains = ['www.athenaspaulista.com.br']
    start_urls = ['http://www.athenaspaulista.com.br/LINHAS/Linhas.htm']

    #~ rules = (
        #~ Rule(SgmlLinkExtractor(allow=r'Linhas.htm'),
        #~ callback='parse', follow=True),
    #~ )

    def parse_routes(self, response):
        """Parses links containing busline route information
       response.meta = dictionary of the type -- (busline, departure): arrival.
       (busline, departure) work as a relational database primary key."""

        hxs = HtmlXPathSelector(response)
        i = response.meta['partial_item']
        i['ida']   = hxs.select('.//div[3]/table/tr//text()').extract()
        i['volta'] = hxs.select('.//div[5]/table/tr//text()').extract()
        
        
        yield i

    def parse(self, response):
        """ Parses the website containing the itineraries
        Uses parse_item as callback for each weblink containing busline
        routes and yields the respective LinhaItems.
        """

        hxs = HtmlXPathSelector(response)
        
        buslines = hxs.select('//td[contains(@width, "56")]/p/b/span/text()')
        buslines = buslines.extract()
        buslinefilter = re.compile('\d\d\d\d')
        buslines = filter(buslinefilter.search, buslines)
        departures = hxs.select('//td[contains(@width, "52")]')
        departures = departures.select('./p/span/text()').extract()
        timefilter = re.compile('\d\d:\d\d', re.IGNORECASE)
        departures = filter(timefilter.search, departures)
        departures.append('-')  # the last 5871 busline has an undefined departure time!

        arrivals = hxs.select('//td[contains(@width, "50")]/p/span/text()')
        arrivals = arrivals.extract()
        arrivals = filter(timefilter.search, arrivals)

        routeURLs = hxs.select('//td[contains(@width, "391")]/p/span/a/@href')
        routeURLs = routeURLs.extract()
        URLprefix = 'http://www.athenaspaulista.com.br/LINHAS/'
        routeURLs = [URLprefix + i for i in routeURLs]

        desc_path = '//td[contains(@width, "391")]/p/span/a/text()'
        descriptions = hxs.select(desc_path).extract()
        descriptions = [i.replace('\r\n', '') for i in descriptions]

        assert len(arrivals) == len(departures) == len(buslines), "Not the same ammount of buslines, departures or arrivals"
        index = 0
        while index < len(arrivals):
            item = LinhaItem()
            item['linha'] = buslines[index]
            item['mpartida'] = departures[index]
            item['mchegada'] = arrivals[index]
            item['link'] = routeURLs[index]
            item['nome'] = descriptions[index]
            if 'X' in item['nome'] and '-' in item['nome']:
                item['origem'], temp = item['nome'].split('X')
                temp = temp.split('-')
                item['destino'], item['via'] = temp[0], temp[1]
            item = Request(item['link'],
                           callback=self.parse_routes,
                           meta={'partial_item': item})
            index += 1
            yield item
