import scrapy


class NHSInformDiseasesSpider(scrapy.Spider):
    name = "nhsinform-diseases"
    diseases = set([])

    def start_requests(self):
        urls = ['https://www.nhsinform.scot/illnesses-and-conditions/a-to-z']
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
        listings = response.xpath("//a[@class='col small-12 medium-6 large-4 module blockgrid-item']/h2/text()").extract()
        for listing in listings:
            disease = listing.strip()
            if ':' in disease:
                parts = disease.split(':')
                disease = parts[0]
            if disease.endswith(')'):
                parts = disease.split('(')
                disease = parts[0]
            self.diseases.add(disease)
            yield {
                'disease': disease
            }
