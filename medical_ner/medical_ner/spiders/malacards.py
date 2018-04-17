import scrapy


class MalacardsSpider(scrapy.Spider):
    name = "malacards"
    diseases = set([])

    def start_requests(self):
        urls = [
            'http://www.malacards.org/categories'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        parts = response.url.split("/")
        if len(parts) == 4:
            # This is the index page
            for category_link in response.xpath('//tr/td/a'):
                url = response.urljoin(category_link.css('::attr(href)').extract_first())
                if response.url.startswith('http://www.malacards.org/categories') or response.url.startswith('https://www.malacards.org/categories'):
                    yield scrapy.Request(url=url, callback=self.parse)
        else:
            for tr in response.xpath('//tr'):
                tds = tr.css('td')
                if len(tds) != 5:
                    continue
                mcid = tds[2].xpath('text()').extract_first()
                disease = tds[3].xpath('a/text()').extract_first()
                if disease not in self.diseases:
                    self.diseases.add(disease)
                    yield {
                        'mcid': mcid,
                        'disease': disease,
                        'category_url': response.url
                    }
