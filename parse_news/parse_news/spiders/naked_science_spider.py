from pathlib import Path

import scrapy


class NakedScienceSpider(scrapy.Spider):
    name = "naked_science"

    def start_requests(self):
        urls = [
            "https://naked-science.ru/article/page/1",
            "https://naked-science.ru/article/page/2",
            "https://naked-science.ru/article/page/3",
            "https://naked-science.ru/article/page/4",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
