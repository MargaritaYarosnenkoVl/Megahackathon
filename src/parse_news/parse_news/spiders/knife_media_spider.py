import datetime
from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class KnifeMediaSpider(scrapy.Spider):
    name: str = "knife_media"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://knife.media/category/news/page/1/",
                  # "https://knife.media/category/news/page/2/",
                  # "https://knife.media/category/news/page/3/",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.widget-news__content"):
            try:
                full_text_link = quote.css("a.widget-news__content-link::attr(href)").get()
                search_words: list[str] = quote.css("a.meta__item::text").getall()
                search_words_cleared: list[str] = await self.clear_search_words(search_words)

                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"title": news_info.get("title"),  # название
                       "brief_text": news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "tag": search_words_cleared[0],  # тэг - одно слово
                       "search_words": " ".join(search_words_cleared),  # слова для поиска
                       "parsed_from": "knife.media",
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(quote.css("time::attr(datetime)").get()),  # дата публикации
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
            title: str = soup.find('h1', {"class": "entry-header__title"}).text
            full_text_list = soup.find('div', {"class": "entry-content"}).findAll("p")
            brief_text = full_text_list[0].text
            full_text = " ".join([p.text.strip() for p in full_text_list[:-1]])

            return {"title": title,
                    "brief_text": brief_text,
                    "full_text": full_text}

    async def clear_search_words(self, words: list[str]) -> list:
        return [word.strip().lower() for word in words]
