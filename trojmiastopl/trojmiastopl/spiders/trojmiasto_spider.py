import scrapy
import os


class StartURLSFromFile:
    def __init__(self):
        print(os.getcwd())
        with open("start_urls.txt", "r") as f:
            self.start_urls = f.read().split("\n")


class TrojmiastoSpider(scrapy.Spider):
    name = "trojmiasto"
    start_urls = StartURLSFromFile().start_urls

    def parse(self, response):
        for poi in response.css("div.basicInfo__item.basicInfo__item--presentationNotPaid"):
            address_info = poi.css("a.objectAddress__link span::text").getall()
            try:
                address = {
                    "city": address_info[0].strip(),
                    "postcode": address_info[1].strip(),
                    "street": address_info[2].strip(),
                }
            except IndexError as e:
                self.logger.error(f"Exception: {e}, Address Info: {address_info}, Reason: {str(e)}")

            res = {
                "name": poi.css("h2 a.objectName__link span::text").get(),
                "categories": poi.css("a.objectTags__item::text").getall(),
                "address": address
            }
            yield res
        next_page = response.css('a[title="następna"]::attr("href")').get()

        if next_page:
            yield response.follow(next_page, self.parse)
