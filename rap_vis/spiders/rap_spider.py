import scrapy
import csv

class RapSpider(scrapy.Spider):
    name = "rapper"
    start_urls = [
        "http://www.ohhla.com/all.html",
        "http://www.ohhla.com/all_two.html",
        "http://www.ohhla.com/all_three.html",
        "http://www.ohhla.com/all_four.html",
        "http://www.ohhla.com/all_five.html"
    ]

    def parse(self, response):
        pre = response.css("PRE")
        for rapper in pre.css("a"):
            with open('rapper.csv', 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow([rapper.css("a::text").get(), rapper.css("a::attr(href)").get()])