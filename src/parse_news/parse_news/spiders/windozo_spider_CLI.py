import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class WindozoSpider(scrapy.Spider):
    name: str = "windozo"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = [f"https://windozo.ru/topics/news/page/1/",
                  f"https://windozo.ru/topics/news/page/2/",
                  f"https://windozo.ru/topics/news/page/3/",
                  f"https://windozo.ru/topics/news/page/4/",
                  f"https://windozo.ru/topics/news/page/5/",
                  f"https://windozo.ru/topics/news/page/6/",
                  f"https://windozo.ru/topics/news/page/7/",
                  f"https://windozo.ru/topics/news/page/8/",
                  f"https://windozo.ru/topics/news/page/9/",
                  f"https://windozo.ru/topics/news/page/10/",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("article.latestPost"):
            full_text_link: str = quote.css("div.post-data h2.title a::attr(href)").get().strip()
            title: str = quote.css("div.readMore a::attr(title)").get().strip()
            brief_text: str = quote.css("div.post-excerpt::text").get().strip()

            news_info: dict = await self.get_news_info(link=full_text_link)
            yield {"title": title,  # название
                   "brief_text": brief_text,  # короткое описание
                   "full_text": news_info.get("full_text").strip().replace('\r', ''),  # полный текст
                   "tag": news_info.get("search_words"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                   "search_words": news_info.get("search_words"),  # строка всех тегов
                   "parsed_from": "windozo.ru",  # название сайта
                   "full_text_link": full_text_link,  # ссылка на полный текст
                   "published_at": news_info.get("published_at"),  # дата публикации
                   "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                   }

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            full_text_list: list[soup] = soup.find("div", {"class": "post-single-content"}).findAll("p")
            search_words = soup.find('meta', {'itemprop': 'name'}).get('content').strip()
            published_at = soup.find('meta', {'property': 'article:published_time'}).get('content').strip()
            return {"full_text": " ".join((p.text.strip() for p in full_text_list)),
                    "search_words": search_words,
                    "published_at": datetime.fromisoformat(published_at)
                    }
