# import os
# import sys
# import time
# from typing import Any, Type
# import scrapy
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerProcess, CrawlerRunner
# from .pipelines import ParseNewsPipeline
# from .spiders import (cnews_spider,
#                       fontanka_spider,
#                       knife_media_spider,
#                       naked_science_spider,
#                       nplus1_spider,
#                       sdelanounas_spider,
#                       techno_news,
#                       windozo_spider,
#                       dnews_spider,
#                       snob_spider
#                       )
#
#
# class SpiderFromCode:
#
#     def __init__(self, name: str):
#         self.settings = {"FEEDS": {f"src/parse_news/parse_news/spiders/json_data/{name}.json": {"format": "json",
#                                                                                                 "overwrite": True}
#                                    },
#                          "ITEM_PIPELINES": {ParseNewsPipeline: 300}}
#         self.runner = CrawlerRunner(self.settings)
#         self.spider_name = name
#
#     def get_spider_by_name(self) -> Type[scrapy.Spider]:
#         spiders = {f"{naked_science_spider.NakedScienceSpider.name}": naked_science_spider.NakedScienceSpider,
#                    f"{cnews_spider.CnewsSpider.name}": cnews_spider.CnewsSpider,
#                    f"{dnews_spider.DNewsSpider.name}": dnews_spider.DNewsSpider,
#                    f"{fontanka_spider.FontankaSpider.name}": fontanka_spider.FontankaSpider,
#                    f"{knife_media_spider.KnifeMediaSpider.name}": knife_media_spider.KnifeMediaSpider,
#                    f"{nplus1_spider.Nplus1Spider.name}": nplus1_spider.Nplus1Spider,
#                    f"{sdelanounas_spider.SdelanoUNasSpider.name}": sdelanounas_spider.SdelanoUNasSpider,
#                    f"{techno_news.TexnoNewsSpider.name}": techno_news.TexnoNewsSpider,
#                    f"{windozo_spider.WindozoSpider.name}": windozo_spider.WindozoSpider,
#                    f"{snob_spider.SnobSpider.name}": snob_spider.SnobSpider,
#                    }
#         return spiders.get(self.spider_name)
#
#     def parse(self):
#         spider = self.get_spider_by_name()
#         # self.process.crawl(spider)
#         # self.process.start()
#         # self.process.stop()
#         self.runner.crawl(spider)
#         d = self.runner.join()
#         d.addBoth(lambda _: self.reactor.stop())
#         self.runner.join()
#         reactor.run()
#         # reactor.callFromThread(reactor.stop)
#         # os._exit(70)
#         # time.sleep(0.2)
#         # os.execl(sys.executable, sys.executable, *sys.argv)
#         # self.runner.crawl(spider)
#         # d = self.runner.join()
#         # self.runner.stop()
#         # d.addBoth(lambda _: reactor.stop())
#         # self.reactor.run()
#
#     def stop(self):
#         # self.reactor.callFromThread(self.reactor.stop)
#         self.runner.join()
#         # self.runner.stop()
#         # self.runner.crawl(NakedScienceSpider)
#         # # self.process.start()
#         # d = self.runner.join()
#         # d.addBoth(lambda _: reactor.stop())
#         # self.reactor.run()
#
#
# if __name__ == "__main__":
#     s = SpiderFromCode("naked_science")
#     s.parse()
