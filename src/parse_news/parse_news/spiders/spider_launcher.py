from typing import Any, Type
import scrapy
import twisted
# from scrapy.crawler import CrawlerProcess, CrawlerRunner
from src.parse_news.parse_news.pipelines import ParseNewsPipeline
from src.parse_news.parse_news.spiders import (cnews_spider,
                                               fontanka_spider,
                                               knife_media_spider,
                                               naked_science_spider,
                                               nplus1_spider,
                                               sdelanounas_spider,
                                               techno_news,
                                               windozo_spider,
                                               dnews_spider,
                                               snob_spider
                                               )


class SpiderFromCode:

    def __init__(self, name: str):
        self.settings = {"FEEDS": {f"src/parse_news/parse_news/spiders/json_data/{name}.json": {"format": "json",
                                                                                                "overwrite": True}
                                   },
                         "ITEM_PIPELINES": {ParseNewsPipeline: 300}}
        # self.process = CrawlerProcess(self.settings)
        self.spider_name = name

    def get_spider_by_name(self) -> Type[scrapy.Spider]:
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
        return spiders.get(self.spider_name)

    def parse(self):
        spider = self.get_spider_by_name(self.spider_name)
        # self.process.crawl(spider)
        # self.process.start()
        # self.process.stop()
        # d = self.runner.crawl(spider)
        # self.runner.crawl(spider)
        # d = self.runner.join()
        # self.runner.stop()
        # d.addBoth(lambda _: reactor.stop())
        # self.reactor.run()

    def stop(self):
        #self.reactor.callFromThread(self.reactor.stop)
        self.runner.join()
        # self.runner.stop()
        # self.runner.crawl(NakedScienceSpider)
        # # self.process.start()
        # d = self.runner.join()
        # d.addBoth(lambda _: reactor.stop())
        # self.reactor.run()


if __name__ == "__main__":
    s = SpiderFromCode("naked_science")
    s.parse()

