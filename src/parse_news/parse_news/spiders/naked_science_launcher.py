import json
from typing import Any, Type
import scrapy
import twisted
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from src.parse_news.parse_news.pipelines import ParseNewsPipeline
from src.parse_news.parse_news.spiders import (cnews_spider_CLI,
                                               fontanka_spider_CLI,
                                               knife_media_spider_CLI,
                                               naked_science_spider_CLI,
                                               nplus1_spider_CLI,
                                               sdelanounas_spider_CLI,
                                               techno_news_CLI,
                                               windozo_spider_CLI,
                                               dnews_spider_CLI,
                                               snob_spider_CLI
                                               )


class SpiderFromCode:

    def __init__(self, name: str):
        self.settings = {"FEEDS": {f"src/parse_news/parse_news/spiders/json_data/{name}.json": {"format": "json",
                                                                                                "overwrite": True}
                                   },
                         "ITEM_PIPELINES": {ParseNewsPipeline: 300}}
        self.runner = CrawlerRunner(self.settings)
        self.reactor: twisted.internet = reactor
        self.spider_name = name

    def get_spider_by_name(self, name: str) -> Type[scrapy.Spider]:
        spiders = {f"{naked_science_spider_CLI.NakedScienceSpider.name}": naked_science_spider_CLI.NakedScienceSpider,
                   f"{cnews_spider_CLI.CnewsSpider.name}": cnews_spider_CLI.CnewsSpider,
                   f"{dnews_spider_CLI.DNewsSpider.name}": dnews_spider_CLI.DNewsSpider,
                   f"{fontanka_spider_CLI.FontankaSpider.name}": fontanka_spider_CLI.FontankaSpider,
                   f"{knife_media_spider_CLI.KnifeMediaSpider.name}": knife_media_spider_CLI.KnifeMediaSpider,
                   f"{nplus1_spider_CLI.Nplus1Spider.name}": nplus1_spider_CLI.Nplus1Spider,
                   f"{sdelanounas_spider_CLI.SdelanoUNasSpider.name}": sdelanounas_spider_CLI.SdelanoUNasSpider,
                   f"{techno_news_CLI.TexnoNewsSpider.name}": techno_news_CLI.TexnoNewsSpider,
                   f"{windozo_spider_CLI.WindozoSpider.name}": windozo_spider_CLI.WindozoSpider,
                   f"{snob_spider_CLI.SnobSpider.name}": snob_spider_CLI.SnobSpider,
                   }
        return spiders.get(name)

    def parse(self):
        spider = self.get_spider_by_name(self.spider_name)
        # d = self.runner.crawl(spider)
        self.runner.crawl(spider)
        d = self.runner.join()
        self.runner.stop()
        # d.addBoth(lambda _: reactor.stop())
        # self.reactor.run()

    def stop(self):
        #self.reactor.callFromThread(self.reactor.stop)
        self.runner.join()
        self.runner.stop()
        # self.runner.crawl(NakedScienceSpider)
        # # self.process.start()
        # d = self.runner.join()
        # d.addBoth(lambda _: reactor.stop())
        # self.reactor.run()


if __name__ == "__main__":
    s = SpiderFromCode("naked_science")
    s.parse()
    s.stop()

