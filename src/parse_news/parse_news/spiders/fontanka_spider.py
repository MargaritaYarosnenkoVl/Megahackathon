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
        target_script_content = response.css("script")[-18].get()  # строка - результат выполнения скрипта
        raw_links: list[tuple] = re.findall(r"""url":"\\u002F(\d{4})\\u002F(\d{2})\\u002F(\d{2})\\u002F(\d{8})""",
                                            string=target_script_content)
        links = ["/".join(link) for link in raw_links]  # соединяем группы
        # print(*links, sep="\n")
        for link in links:
            try:
                full_text_link: str = "https://www.fontanka.ru/" + link + "/"
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"title": news_info.get("title"),  # название
                       "brief_text": news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": news_info.get("tag"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "fontanka.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.strptime(response.url[24:34], "%Y/%m/%d"),  # дата публикации
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
            title = soup.find("h1", {"itemprop": "http://schema.org/headline"}).text.strip()
            tag = soup.find("h4", {"itemprop": "name"}).text.strip()
            brief_text = soup.find("section", {"itemprop": "articleBody"}).find("p").text.strip()
            full_text_list: list[soup] = soup.find("section", {"itemprop": "articleBody"}).findAll("p")
            # search_words: list[soup] = soup.findAll('a', {'itemprop': 'about'})
            published_at = soup.find("span", {"itemprop": "datePublished"}).text.strip()
            return {"title": title,
                    "tag": tag,
                    "brief_text": brief_text,
                    "full_text": " ".join((p.text.strip() for p in full_text_list)),
                    "search_words": tag,
                    "published_at": published_at
                    }
