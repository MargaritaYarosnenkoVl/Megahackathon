import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from src.parse_news.parse_news.spiders.naked_science_spider_CLI import NakedScienceSpider
from src.parse_news.parse_news.pipelines import ParseNewsPipeline


class SpiderFromCode:

    def __init__(self):
        self.settings = {"FEEDS": {"src/parse_news/parse_news/spiders/json_data/naked_science.json": {"format": "json",
                                                                                                      "overwrite": True}
                                   },
                         "ITEM_PIPELINES": {ParseNewsPipeline: 300}}
        self.runner = CrawlerRunner(self.settings)
        self.reactor = reactor

    def parse(self):
        d = self.runner.crawl(NakedScienceSpider)
        d.addBoth(lambda _: reactor.stop())
        self.reactor.run()


        # self.runner.crawl(NakedScienceSpider)
        # # self.process.start()
        # d = self.runner.join()
        # d.addBoth(lambda _: reactor.stop())
        # self.reactor.run()


if __name__ == "__main__":
    s = SpiderFromCode()
    s.parse()
