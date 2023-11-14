import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class Nplus1Spider(scrapy.Spider):
    name: str = "nplus1"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}
    today = datetime.today()
    today_1 = today - timedelta(days=1)
    today_2 = today - timedelta(days=2)
    today_3 = today - timedelta(days=3)
    today_4 = today - timedelta(days=4)
    today_5 = today - timedelta(days=5)
    today_6 = today - timedelta(days=6)

    start_urls = [f"https://nplus1.ru/news/{today.year}/{today.month}/{today.day}",
                  f"https://nplus1.ru/news/{today_1.year}/{today_1.month}/{today_1.day}",
                  f"https://nplus1.ru/news/{today_2.year}/{today_2.month}/{today_2.day}",
                  f"https://nplus1.ru/news/{today_3.year}/{today_3.month}/{today_3.day}",
                  f"https://nplus1.ru/news/{today_4.year}/{today_4.month}/{today_4.day}",
                  f"https://nplus1.ru/news/{today_5.year}/{today_5.month}/{today_5.day}",
                  f"https://nplus1.ru/news/{today_6.year}/{today_6.month}/{today_6.day}",
                  ]

    async def parse(self, response, **kwargs):
        target_script_content = response.css("script").getall()[3]  # строка - результат выполнения скрипта
        links_origin_str: str = target_script_content[41:-15]  # json строка с данными, не парсится scrapy & bs
        raw_links: list[str] = re.findall(r"https:\\\\\\/\\\\\\/nplus1\.ru\\\\\\/news\\\\\\/\d{4}\\\\\\/\d{2}\\\\\\/\d{2}\\\\\\/[\w|-]*",
                                          string=links_origin_str)  # список ссылок на статьи в этот день
        links = [link.replace("\\\\\\", "") for link in raw_links]  # удаляем лишние символы из ссылок

        for full_text_link in links:
            news_info: dict = await self.get_news_info(link=full_text_link)

            yield {"title": news_info.get("title"),  # название
                   "brief_text": news_info.get("title") + news_info.get("brief_text"),  # короткое описание
                   "full_text": news_info.get("full_text"),  # полный текст
                   "tag": news_info.get("tag"),  # тэг - одно слово
                   "search_words": "",  # слова для поиска
                   "full_text_link": full_text_link,  # ссылка на полный текст
                   "published_at": datetime.strptime((response.url[25:]), "%y/%m/%d"),  # дата публикации
                   "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                   }

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            title: str = soup.find('h1', {"class": "text-34"}).text.strip()
            full_text_list: list[soup] = soup.findAll('p', {"class": "mb-6"})
            tag: str = soup.find('div', {"class": "content-start"}).findAll('a', {"class": "group"})[2].text.strip()

            return {"title": title,
                    "brief_text": full_text_list[0].text.strip(),
                    "full_text": " ".join((p.text.strip() for p in full_text_list)),
                    "tag": tag
                    }

