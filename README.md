# web-scrapers
This is a repository for my web-scraping projects.

## Requirements
- python 3.5+
- [scrapy] 1.5+

## Text Summarization
News articles and their bullet-point summaries scraped from Times of India News Archive.

## Medical NER
Diseases and treatments/tests scraped from medical websites. Following gazetteers have been been created:
1. **[malacards-diseases]** scraped from [malacards.org](https://www.malacards.org/categories/) (18455 entries).
2. **[medicinenet-diseases]** scraped from [medicinenet.com](https://www.medicinenet.com/diseases_and_conditions/alpha_a.htm) (4969 entries). 
3. **[medicinenet-treatments]** scraped from [medicinenet.com](https://www.medicinenet.com/procedures_and_tests/alpha_a.htm) (931 entries).

## References
- http://sangaline.com/post/advanced-web-scraping-tutorial/

[scrapy]: https://scrapy.org/
[malacards-diseases]: https://github.com/Shivanshu-Gupta/web-scrapers/blob/master/medical_ner/malacards-diseases.json
[medicinenet-diseases]: https://github.com/Shivanshu-Gupta/web-scrapers/blob/master/medical_ner/medicinenet-diseases.json
[medicinenet-treatments]: https://github.com/Shivanshu-Gupta/web-scrapers/blob/master/medical_ner/medicinenet-treatments.json
