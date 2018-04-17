import scrapy


class MedicineNetTreatmentsSpider(scrapy.Spider):
    name = "medicinenet-treatments"
    procedures = set([])

    def start_requests(self):
        urls = ['https://www.medicinenet.com/procedures_and_tests/alpha_{}.htm'.format(chr(i)) for i in range(97, 123)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _process_comma(self, entity):
        names = [entity]
        parts = entity.split(',')
        if len(parts) == 2:
            names.append(parts[1].strip() + ' ' + parts[0].strip())
        else:
            # either no comma or multiple commas - just return what's already found
            pass
        return names

    def _process_brackets(self, text):
        '''
            process the listing text to create a more extensive gazeteer.
            - extract names within brackets as often contain synonyms. eg.: Gilles de la Tourette Syndrome (Tourette Syndrome)
            - for comma separated entries like 'Glands, Swollen Lymph' also add 'Swollen Lymph Glands'
        '''
        stack = [[]]
        for char in text:
            if char == '(':
                stack.append([])
            elif char == ')':
                entity = ''.join(stack.pop()).strip()
                for name in self._process_comma(entity):
                    yield name
            else:
                stack[-1].append(char)
        entity = ''.join(stack.pop()).strip()
        for name in self._process_comma(entity):
            yield name

    def parse(self, response):
        print(response.url)
        listings = response.xpath("//div[@class='AZ_results']/ul/li/a/text()").extract()
        for listing in listings:
            for procedure in self._process_brackets(listing):
                if procedure in self.procedures:
                    continue
                self.procedures.add(procedure)
                yield {
                    'procedure': procedure
                }
