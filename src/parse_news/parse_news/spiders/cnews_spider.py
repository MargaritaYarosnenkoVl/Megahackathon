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
    RU_MONTH_VALUES = {
        'Января': "01",
        'Февраля': "02",
        'Марта': "03",
        'Апреля': "04",
        'Мая': "05",
        'Июня': "06",
        'Июля': "07",
        'Августа': "08",
        'Сентября': "09",
        'Октября': "10",
        'Ноября': "11",
        'Декабря': "12",
    }

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
        for quote in response.css("div.allnews_item"):
            full_text_link: str = quote.css("a::attr(href)").get().strip()
            title: str = quote.css("a::text").get().strip()

            news_info: dict = await self.get_news_info(link=full_text_link)
            try:
                yield {"title": title,  # название
                       "brief_text": title + " " + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": "",  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": "",  # строка всех тегов
                       "parsed_from": "cnews.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": news_info.get("published_at"),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }
            except AttributeError as e:
                print(e, full_text_link)
                continue
            except TypeError as e:
                print(e, full_text_link)
                continue
            except IndexError as e:
                print(e, full_text_link)
                continue

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link.replace("http", "https"), headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            brief_text: str = soup.find("article", {"class": "news_container"}).find("p").text.strip()
            full_text: list[soup] = soup.find("article", {"class": "news_container"}).findAll("p")
            # search_words: ОТСУТСТВУЮТ!
            published_at = soup.find("div", {"class": "article_date"}).find("time", {"class": "article-date-desktop"}).text.strip()
            for old, new in self.RU_MONTH_VALUES.items():
                published_at = re.sub(old, new, published_at)

            return {"brief_text": brief_text,
                    "full_text": " ".join(p.text.strip() for p in full_text),
                    # "search_words": " ".join((word.text.strip().lower() for word in search_words))
                    "published_at": datetime.strptime(published_at, "%d %m %Y %H:%M")
                    }
