import datetime
from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime


class NakedScienceSpider(scrapy.Spider):
    name: str = "naked_science"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://naked-science.ru/article/page/1",
                  # "https://naked-science.ru/article/page/2",
                  # "https://naked-science.ru/article/page/3",
                  # "https://naked-science.ru/article/page/4",
                  ]

    async def parse(self, response, **kwargs):
        for quote in response.css("div.news-item.grid"):
            try:
                full_text_link: str = quote.css("a::attr(href)").get()
                search_words: list = quote.css("div.terms-item a.animate-custom::text").getall()
                search_words_cleared: list = await self.clear_search_words(search_words)

                yield {"title": quote.css("a::text").get(),  # название
                       "brief_text": quote.css("p::text").get(),  # короткое описание
                       "full_text": await self.get_full_text(link=full_text_link),  # полный текст
                       "tag": "наука",  # тэг - одно слово
                       "search_words": " ".join(search_words_cleared),  # слова для поиска
                       "parsed_from": "naked-science.ru",
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(quote.css("span::attr(data-published)").get()),  # дата публикации
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }
            except AttributeError as e:
                print(e)
                continue

    async def get_full_text(self, link: str) -> str:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            post_lead: str = soup.find('div', {"class": "post-lead"}).text
            paragraphs = soup.find('div', {"class": "body"}).findAll("p")
            full_t = post_lead.strip() + " " + " ".join((p.text.strip() for p in paragraphs))
            return full_t

    async def clear_search_words(self, words: list[str]) -> list:
        return [word.strip()[2:] if word.startswith("#") else word.strip().lower() for word in words]
