import datetime
from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class DNewsSpider(scrapy.Spider):
    name: str = "news3d"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://3dnews.ru/news/page-1.html",
                  "https://3dnews.ru/news/page-2.html",
                  "https://3dnews.ru/news/page-3.html",
                  "https://3dnews.ru/news/page-4.html",
                  "https://3dnews.ru/news/page-5.html",
                  "https://3dnews.ru/news/page-6.html",
                  "https://3dnews.ru/news/page-7.html",
                  "https://3dnews.ru/news/page-8.html",
                  "https://3dnews.ru/news/page-9.html",
                  "https://3dnews.ru/news/page-10.html",
                  "https://3dnews.ru/news/page-11.html",
                  "https://3dnews.ru/news/page-12.html",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.article-entry"):
            try:
                full_text_link: str = "https://3dnews.ru" + quote.css("a.entry-header::attr(href)").get().strip()
                title = quote.css("a.entry-header h1::text").get().strip()
                brief_text = quote.css("p::text").get()
                published_at = quote.css("span.entry-date::text").get().strip()

                news_info: dict = await self.get_news_info(link=full_text_link)

                print(response.url[24:35])
                yield {"title": title,  # название
                       "brief_text": brief_text,  # короткое описание
                       "full_text": news_info.get("full_text").strip(),  # полный текст
                       "tag": news_info.get("tag"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "parsed_from": "3dnews.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.strptime(published_at, "%d.%m.%Y %H:%M"),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }
            except AttributeError as e:
                print(e)
                continue
            except TypeError as e:
                print(e)
                continue
            except IndexError as e:
                print(e)
                continue

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            full_text_list: list[soup] = soup.find("div", {"class": "entry-body"}).findAll("p")
            search_words: list[soup] = soup.find('div', {'class': 'catlist'}).findAll('a')
            tags = soup.find('div', {'class': 'taglist'}).findAll('a')
            return {"full_text": " ".join((p.text.strip() for p in full_text_list)),
                    "search_words": " ".join((a.text.strip() for a in search_words)),
                    "tags": " ".join((a.text.strip() for a in tags)),
                    }
