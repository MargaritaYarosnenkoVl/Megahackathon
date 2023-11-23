import datetime
from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class TexnoNewsSpider(scrapy.Spider):
    name: str = "techno_news"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://techno-news.net/page/1/",
                  "https://techno-news.net/page/2/",
                  "https://techno-news.net/page/3/",
                  "https://techno-news.net/page/4/",
                  "https://techno-news.net/page/5/",
                  "https://techno-news.net/page/6/",
                  "https://techno-news.net/page/7/",
                  "https://techno-news.net/page/8/",
                  "https://techno-news.net/page/9/",
                  "https://techno-news.net/page/10/",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.inside-article"):
            try:
                full_text_link: str = quote.css("h2.entry-title a::attr(href)").get().strip()
                title = quote.css("a[rel='bookmark']::text").get().strip()
                brief_text = quote.css("div.entry-summary p::text").get().strip()
                tag = quote.css("div.entry-meta a::text").get().strip()
                published_at = quote.css("div.entry-meta span::text").get().strip()

                news_info: dict = await self.get_news_info(link=full_text_link)

                print(response.url[24:35])
                yield {"title": title.replace(' ', ' '),  # название
                       "brief_text": brief_text,  # короткое описание
                       "full_text": news_info.get("full_text").strip().replace('\t', ''),  # полный текст
                       "tag": tag,  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": tag,  # строка всех тегов
                       "parsed_from": "techno-news.net",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.strptime(published_at, "%H:%M %d-%m-%Y"),  # дата публикации
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
            full_text_list: list[soup] = soup.find("div", {"class": "entry-content"}).findAll("p")
            full_text = " ".join([p.text for p in full_text_list])
            return {"full_text": full_text}
