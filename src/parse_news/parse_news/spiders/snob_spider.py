import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class SnobSpider(scrapy.Spider):
    name: str = "snob"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = [f"https://snob.ru/news/?page=1",
                  f"https://snob.ru/news/?page=2",
                  f"https://snob.ru/news/?page=3",
                  f"https://snob.ru/news/?page=4",
                  f"https://snob.ru/news/?page=5",
                  f"https://snob.ru/news/?page=6",
                  f"https://snob.ru/news/?page=7",
                  f"https://snob.ru/news/?page=8",
                  f"https://snob.ru/news/?page=9",
                  f"https://snob.ru/news/?page=10",
                  f"https://snob.ru/news/?page=11",
                  f"https://snob.ru/news/?page=12",
                  f"https://snob.ru/news/?page=13",
                  f"https://snob.ru/news/?page=14",
                  f"https://snob.ru/news/?page=15",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.col-entry a"):
            link_quote: str = quote.css("a::attr(href)").get()
            if not link_quote.startswith("https:"):
                full_text_link = "https://snob.ru" + link_quote
                title = quote.css("a div.title::text").get().strip()

                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"title": title,  # название
                       "brief_text": title + " " + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": news_info.get("tag"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "snob.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": news_info.get("published_at"),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            brief_text: str = soup.find("div", {"class": "lead"}).find("p").text.strip()
            full_text_list: list[soup] = soup.find("div", {"class": "text"}).findAll("p")
            full_text: str = " ".join((p.text for p in full_text_list))
            search_words: list[soup] = soup.find("div", {"class": "entry__tags"}).findAll("a")
            published_at = soup.find("meta", {"name": "datePublished"})["content"]

            return {"brief_text": brief_text,
                    "full_text": full_text,
                    "search_words": " ".join((word.text[1:].strip().lower() for word in search_words)),
                    "tag": search_words[-1].text[1:].strip().lower(),
                    "published_at": datetime.fromisoformat(published_at)
                    }
