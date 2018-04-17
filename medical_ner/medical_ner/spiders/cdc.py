import scrapy


class CDCSpider(scrapy.Spider):
    name = "cdc"
    procedures = set([])

    def start_requests(self):
        urls = ['https://www.cdc.gov/az/{}.html'.format(chr(i)) for i in range(97, 123)]
        urls.append('https://www.cdc.gov/az/0.html')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def process(self, text):
        stack = [[]]
        for char in text:
            if char == '(':
                stack.append([])
            elif char == ')':
                yield ''.join(stack.pop()).strip()
            else:
                stack[-1].append(char)
        yield ''.join(stack.pop()).strip()

    def parse(self, response):
        print(response.url)
        listings = response.xpath("//div[@class='AZ_results']/ul/li/a/text()").extract()
        for listing in listings:
            for procedure in self.process(listing):
                if procedure in self.procedures:
                    continue
                self.procedures.add(procedure)
                yield {
                    'procedure': procedure
                }
