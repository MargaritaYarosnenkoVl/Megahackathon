import datetime
# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  #, timedelta


class PortalKultura(scrapy.Spider):
    name: str = "portal_kultura"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = [f"https://portal-kultura.ru/articles/news/?SECTION_CODE=news",
                  # f"https://portal-kultura.ru/articles/news/?SECTION_CODE=news&PAGEN_4=2",
                  # f"https://portal-kultura.ru/articles/news/?SECTION_CODE=news&PAGEN_4=3",
                  # f"https://portal-kultura.ru/articles/news/?SECTION_CODE=news&PAGEN_4=4",
                  # f"https://portal-kultura.ru/articles/news/?SECTION_CODE=news&PAGEN_4=5",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.link-article"):
            try:
                link_quote: str = quote.css("a::attr(href)").get()

                full_text_link = "https://portal-kultura.ru" + link_quote
                title = quote.css("h2 a::text").get().replace(' ', ' ')

                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"title": title,  # название
                       "brief_text": title + " " + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text").replace(' ', ' ').replace('\r', '').replace('\n', ''),
                       # полный текст
                       "tag": "культура",  # quote.css("div.entry__tags a::text").get(),  # тэг - тема новости
                       # (первое слово/фраза из группы тегов)
                       "search_words": "культура",  # news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "portal-kultura.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": news_info.get("published_at"),  # дата публикации
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
            brief_text = soup.select_one('.block-article div b').text.replace(' ', ' ').replace('\r', '').replace('\n', '')
            full_text_list = soup.select('.block-article div:not(.detail-picture-wrap)')
            full_text = " ".join([p.text.strip() for p in full_text_list])
            # search_words: list[soup] = soup.find("div", {"class": "entry__tags"}).findAll("a")
            published_at = soup.find("p", {"class": "date"}).text.strip()

            return {"brief_text": brief_text,
                    "full_text": full_text,
                    # "search_words": " ".join((word.text.lower() for word in search_words)),
                    "published_at": datetime.strptime(published_at, "%d.%m.%Y")
                    }
