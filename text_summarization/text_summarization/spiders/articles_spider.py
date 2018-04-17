import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    article_ids = set([])
    n_parsed = 0

    def start_requests(self):
        urls = [
            # 'http://timesofindia.indiatimes.com/india/kulbhushan-jadhav-held-on-concocted-charges-10-things-india-said-at-the-icj/articleshow/58682916.cms',
            # 'http://timesofindia.indiatimes.com/india/india-fears-kulbhushan-jadhav-could-be-executed-before-icj-trial-ends/articleshow/58684179.cms',
            # 'http://timesofindia.indiatimes.com/india/cbi-examines-ex-haryana-cm-hooda-in-alleged-land-scam/articleshow/58682870.cms'
            'http://timesofindia.indiatimes.com/2017/2/23/archivelist/year-2017,month-2,starttime-42789.cms'
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
