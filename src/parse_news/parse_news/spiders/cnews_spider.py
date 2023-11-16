import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class CnewsSpider(scrapy.Spider):
    name: str = "cnews"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}
    day = datetime.today()
    day_4 = day - timedelta(days=4)

    start_urls = [f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/section_0",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_2",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_3",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_4",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_5",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_6",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_7",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_8",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_9",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_10",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_11",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_12",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_13",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_14",
                  f"https://www.cnews.ru/archive/date_{day_4.day}.{day_4.month}.{day_4.year}_{day.day}.{day.month}.{day.year}/type_top_lenta/page_15",
                  ]

    async def parse(self, response, **kwargs):
        quote: str = response.css("div.allnews_mainpage").get()
        links: list = re.findall(r"http:\/\/\w*\.cnews\.ru\/news\/line\/\d{4}-\d{2}-\d{2}_[\w|_|\-|:]*", quote)
        titles: list = re.findall(r'<a href="http:\/\/\w*\.cnews\.ru\/news\/line\/\d{4}-\d{2}-\d{2}_[\w|_|\-|:]*".*>(.*)</a>', quote)

        for full_text_link, title in zip(links, titles):
            news_info: dict = await self.get_news_info(link=full_text_link)
            try:
                yield {"title": title,  # название
                       "brief_text": title + " " + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": news_info.get("tag"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "Cnews",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": news_info.get("published_at"),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }
            except AttributeError:
                yield {"title": title,  # название
                       "brief_text": "brief_text",  # короткое описание
                       "full_text": "full_text",  # полный текст
                       "tag": "tag",  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": "search_words",  # строка всех тегов
                       "parsed_from": "Cnews",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": "published_at",  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link.replace("http", "https"), headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            brief_text: str = soup.find("article", {"class": "news_container"}).find("p").text.strip()
            full_text: list[soup] = soup.find("article", {"class": "news_container"}).findAll("p")
            # search_words: ОТСУТСТВУЮТ!
            published_at = soup.find("div", {"class": "article_date"}).find("time", {"class": "article-date-desktop"}).text.strip()

            return {"brief_text": brief_text,
                    "full_text": " ".join(p.text.strip() for p in full_text),
                    # "search_words": " ".join((word.text.strip().lower() for word in search_words))
                    "published_at": published_at
                    }
