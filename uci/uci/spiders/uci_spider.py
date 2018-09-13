import scrapy

from uci.items import UciItem

class UciSpider(scrapy.Spider):
    name = "uci"
    allowed_urls = ["https://archive.ics.uci.edu/ml/datasets.html"]
    start_urls = [
            "https://archive.ics.uci.edu/ml/datasets.html"
            ]

    def parse(self, response):
        # if this is the overview page:
        if response.url == 'https://archive.ics.uci.edu/ml/datasets.html':
            for href in response.css(".normal > b > a::attr('href')"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse)
        else:
            # if this is a dataset page:
            item = UciItem()
            item['url'] = response.url

            name = ('/html/body/table[2]/tr/td/table[1]/'
                    'tr/td[1]/p[1]/span[1]/b/text()')

            tmp = response.xpath(name).extract()
            if len(tmp) == 0:
                return
            item['name'] = response.xpath(name).extract()[0]
            if item['name'].endswith('Data Set'):
                item['name'] = item['name'][:-8]

            dset_char = ('/html/body/table[2]/tr/td/table[2]/tr[1]/td[2]/p/text()')
            item['dset_characteristics'] = response.xpath(dset_char).extract()[0]
            attr_char = ('/html/body/table[2]/tr/td/table[2]/tr[2]/td[2]/p/text()')
            item['attr_characteristics'] = response.xpath(attr_char).extract()[0]
            area = ('/html/body/table[2]/tr/td/table[2]/tr[1]/td[6]/p/text()')
            item['area'] = response.xpath(area).extract()[0]

            instances = ('/html/body/table[2]/tr/td/table[2]/tr[1]/td[4]/p/text()')
            item['instances'] = response.xpath(instances).extract()[0]
            if item['instances'].isdigit():
                item['instances'] = int(item['instances'])

            attributes = ('/html/body/table[2]/tr/td/table[2]/'
                    'tr[2]/td[4]/p/text()')
            item['attributes'] = response.xpath(attributes).extract()[0]
            if item['attributes'].isdigit():
                item['attributes'] = int(item['attributes'])

            missing = ('/html/body/table[2]/tr/td/table[2]/tr[3]/td[4]/p/text()')
            item['missings'] = response.xpath(missing).extract()[0]

            task = ('/html/body/table[2]/tr/td/table[2]/tr[3]/td[2]/p/text()')
            item['tasks'] = response.xpath(task).extract()[0]
            date = ('/html/body/table[2]/tr/td/table[2]/tr[2]/td[6]/p/text()')
            item['date'] = response.xpath(date).extract()[0]

            hits = ('/html/body/table[2]/tr/td/table[2]/tr[3]/td[6]/p/text()')
            item['hits'] = response.xpath(hits).extract()[0]
            if item['hits'].isdigit():
                item['hits'] = int(item['hits'])
            yield item

