import scrapy


class MedicineNetSpider(scrapy.Spider):
    name = "medicinenet"
    procedures = set([])

    def start_requests(self):
        urls = ['https://www.medicinenet.com/procedures_and_tests/alpha_{}.htm'.format(chr(i)) for i in range(97, 123)]
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
