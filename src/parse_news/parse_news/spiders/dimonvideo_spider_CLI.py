import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class DimonVideoSpider(scrapy.Spider):
    name: str = "dimonvideo"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = [f"https://dimonvideo.ru/usernews/1/0/dateD/0",
                  f"https://dimonvideo.ru/usernews/1/0/dateD/10",
                  f"https://dimonvideo.ru/usernews/1/0/dateD/20",
                  f"https://dimonvideo.ru/usernews/1/0/dateD/30",
                  f"https://dimonvideo.ru/usernews/1/0/dateD/40",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("article.message"):
            try:
                link_quote: str = quote.css("div.entry-title b a::attr(href)").get().strip()
                if not link_quote.startswith("https:"):
                    full_text_link = "https://dimonvideo.ru/" + link_quote
                    title = quote.css("div.entry-title b a::attr(title)").get().replace(' ', ' ')
                    tag = quote.css("span[style='vertical-align: middle'] a::text").get()
                    published_at = quote.css("span[style='vertical-align: middle'] time::attr(datetime)").get()
                    brief_text = quote.css("div.opisanie p::text").get().strip()
                    # quote.css("div.opisanie p:nth-of-type(2)")[0].text.strip()

                    news_info: dict = await self.get_news_info(link=full_text_link)

                    yield {"title": title,  # название
                           "brief_text":  brief_text,  # короткое описание
                           "full_text": news_info.get("full_text").replace(' ', ' '),  # полный текст
                           "tag": tag,  # тэг - тема новости (первое слово/фраза из группы тегов)
                           "search_words": tag,  # строка всех тегов
                           "parsed_from": "dimonvideo.ru",  # название сайта
                           "full_text_link": full_text_link,  # ссылка на полный текст
                           "published_at": datetime.fromisoformat(published_at[:-1]),  # дата публикации
                           "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                           }
            except AttributeError as e:
                print(e)
                continue
            except IndexError as e:
                print(e)
                continue
            except TypeError as e:
                print(e)
                continue

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            full_text_list: list[soup] = soup.find("div", {"class": "opisanie"}).findAll("p")
            full_text = " ".join([p.text for p in full_text_list])

            return {
                    "full_text": full_text,
                    }
