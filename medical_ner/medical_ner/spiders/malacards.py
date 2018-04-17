import scrapy


class MalacardsSpider(scrapy.Spider):
    name = "articles"
    article_ids = set([])
    n_parsed = 0

    def start_requests(self):
        urls = [
            'http://www.malacards.org/categories'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        summarybox = response.xpath("//span[@class='hsummary']")
        if summarybox != []:
            # extract summary
            summary = ''
            if summarybox.css('artsummary') != []:
                if summarybox.css('artsummary ul') != []:
                    summary = summarybox.xpath('artsummary/ul/li/text()').extract()
                elif summarybox.css('artsummary ol') != []:
                    summary = summarybox.xpath('artsummary/ol/li/text()').extract()
            else:
                summary = summarybox.xpath("text()").extract_first()
            summary = ' '.join(summary)

            # extract article
            article_xpaths = [
                "//div[@class='section1']/div[@class='Normal']/text()",
                "//div[@class='section1']/div[@class='Normal']/span/text()",
                "//div[@class='section1']/div[@class='Normal']/a/text()"]
            content = response.xpath('|'.join(article_xpaths))
            content = [line.strip() for line in content.extract()]
            article = ' '.join([line for line in content if line != ''])
            self.n_parsed = self.n_parsed + 1
            print(self.n_parsed, '\t: ', response.url)
            yield {
                'url': response.url,
                'summary': summary,
                'article': article
            }

        # follow article links
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if '/articleshow/' in url:
                if not url.startswith('http://'):
                    url = 'http://timesofindia.indiatimes.com/' + url
                if url.startswith('http://timesofindia.indiatimes.com/'):
                    parts = url.split("/")
                    article_id = int(parts[-1].split('.')[0])
                    if article_id not in self.article_ids:
                        self.article_ids.add(article_id)
                        yield scrapy.Request(url=url, callback=self.parse)
