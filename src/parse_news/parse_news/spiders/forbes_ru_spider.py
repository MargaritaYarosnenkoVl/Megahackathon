import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class Nplus1Spider(scrapy.Spider):
    name: str = "forbes"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://www.forbes.ru/new?page=1",
                  # "https://www.forbes.ru/new?page=2",
                  # "https://www.forbes.ru/new?page=3",
                  # "https://www.forbes.ru/new?page=4",
                  # "https://www.forbes.ru/new?page=5",
                  # "https://www.forbes.ru/new?page=6",
                  # "https://www.forbes.ru/new?page=7",
                  # "https://www.forbes.ru/new?page=8",
                  # "https://www.forbes.ru/new?page=9",
                  # "https://www.forbes.ru/new?page=10",
                  ]

    async def parse(self, response, **kwargs):
        target_script_content = response.css("script").getall()[0]  # строка - результат выполнения скрипта
        raw_links: list[str] = re.findall(r"""url_alias:"(\w*)\\u002F([\w|-]*)""", target_script_content)
        links = ["/".join(link) for link in raw_links]  # соединяем группы
        # print(*links, sep='\n')
        for link in links:
            try:
                full_text_link = "https://www.forbes.ru/" + link
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"title": news_info.get("title"),  # название
                       "brief_text": news_info.get("title") + news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": news_info.get("tag"),  # тэг - одно слово
                       "search_words": news_info.get("tag"),  # слова для поиска
                       "parsed_from": "forbes.ru",
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(news_info.get("published_at")),  # дата публикации
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
            title = soup.find("h1", {"itemprop": "headline"}).text.strip()
            tag = soup.find("a", {"itemprop": "item"}).find("span").text.strip()
            brief_text = soup.find("strong", {"itemprop": "articleBody"}).text.strip()
            full_text_list: list[soup] = soup.findAll("p", {"itemprop": "articleBody"})
            search_words: list[soup] = soup.findAll('a', {'itemprop': 'about'})
            published_at = soup.find("time", {"itemprop": "datePublished"})["datetime"]
            return {"title": title,
                    "tag": tag,
                    "brief_text": brief_text,
                    "full_text": " ".join((p.find("span").text.strip() for p in full_text_list)),
                    "search_words": " ".join((a.find("span").text.strip() for a in search_words)),
                    "published_at": published_at
                    }

