import datetime
from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class SdelanoUNasSpider(scrapy.Spider):
    name: str = "sdelanounas"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://sdelanounas.ru/blogs/?page=0",
                  # "https://sdelanounas.ru/blogs/?page=1",
                  # "https://sdelanounas.ru/blogs/?page=2",
                  # "https://sdelanounas.ru/blogs/?page=3",
                  # "https://sdelanounas.ru/blogs/?page=4",
                  # "https://sdelanounas.ru/blogs/?page=5",
                  # "https://sdelanounas.ru/blogs/?page=6",
                  # "https://sdelanounas.ru/blogs/?page=7",
                  # "https://sdelanounas.ru/blogs/?page=8",
                  # "https://sdelanounas.ru/blogs/?page=9",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("li.post"):
            try:
                full_text_link: str = "https://sdelanounas.ru" + quote.css("h2 a::attr(href)").get().strip()
                title = quote.css("h2 a::text").get().strip()
                brief_text_ = quote.css("p::text").getall()
                tag = quote.css("div.theme a::text").get().strip()
                published_at = quote.css("div.info li.time time::attr(datetime)").get().strip()

                news_info: dict = await self.get_news_info(link=full_text_link)

                print(response.url[24:35])
                yield {"title": title,  # название
                       "brief_text": " ".join([p.strip() for p in brief_text_]),  # короткое описание
                       "full_text": news_info.get("full_text").strip(),  # полный текст
                       "tag": tag,  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "sdelanounas.ru",  # название сайта
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
            full_text_list: list[soup] = soup.find("div", {"class": "text"}).findAll("p")
            search_words = soup.find('div', {'class': 'tags'}).findAll('a')
            # published_at = soup.find('meta', {'property': 'article:published_time'}).get('content')
            return {"full_text": " ".join((p.text.strip() for p in full_text_list)),
                    "search_words": " ".join((a.text.strip() for a in search_words)),
                    }
