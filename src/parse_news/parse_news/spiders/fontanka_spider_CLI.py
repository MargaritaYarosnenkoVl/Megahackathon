import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class FontankaSpider(scrapy.Spider):
    name: str = "fontanka"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}
    today = datetime.today()
    today_1 = today - timedelta(days=1)
    today_2 = today - timedelta(days=2)
    today_3 = today - timedelta(days=3)
    today_4 = today - timedelta(days=4)
    today_5 = today - timedelta(days=5)
    today_6 = today - timedelta(days=6)

    start_urls = [f"https://www.fontanka.ru/{today.year}/{'%02d' % today.month}/{'%02d' % today.day}/all.html",
                  f"https://www.fontanka.ru/{today_1.year}/{'%02d' % today_1.month}/{'%02d' % today_1.day}/all.html",
                  f"https://www.fontanka.ru/{today_2.year}/{'%02d' % today_2.month}/{'%02d' % today_2.day}/all.html",
                  f"https://www.fontanka.ru/{today_3.year}/{'%02d' % today_3.month}/{'%02d' % today_3.day}/all.html",
                  f"https://www.fontanka.ru/{today_4.year}/{'%02d' % today_4.month}/{'%02d' % today_4.day}/all.html",
                  f"https://www.fontanka.ru/{today_5.year}/{'%02d' % today_5.month}/{'%02d' % today_5.day}/all.html",
                  f"https://www.fontanka.ru/{today_6.year}/{'%02d' % today_6.month}/{'%02d' % today_6.day}/all.html",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("li.IHafh"):
            link_quote: str = quote.css("a.IHb9::attr(href)").get()
            if not link_quote.startswith("https:"):
                full_text_link = "https://www.fontanka.ru" + link_quote
                title = quote.css("a.IHb9::text").get()

                news_info: dict = await self.get_news_info(link=full_text_link)
                yield {"title": title,  # название
                       "brief_text": title + " " + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": quote.css("a.IHf3::attr(title)").get(),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "fontanka.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.strptime(response.url[24:34], "%Y/%m/%d"),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            full_text: list[soup] = soup.find("div", {"class": "JNfp"}).findAll("p")
            brief_text = full_text[1].text.strip()
            search_words: list[soup] = soup.findAll("h4", {"class": "A7f3"})

            return {"brief_text": brief_text,
                    "full_text": " ".join((p.text.strip() for p in full_text)),
                    "search_words": " ".join((word.text.strip().lower() for word in search_words)),
                    }
