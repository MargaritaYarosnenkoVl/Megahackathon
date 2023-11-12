import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import scrapy
from datetime import datetime


class NakedScienceSpider(scrapy.Spider):
    name: str = "naked_science"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = [
        "https://naked-science.ru/article/page/1",
        "https://naked-science.ru/article/page/2",
        "https://naked-science.ru/article/page/3",
        "https://naked-science.ru/article/page/4",
    ]

    # def start_requests(self):
    #     urls = [
    #         "https://naked-science.ru/article/page/1",
    #         "https://naked-science.ru/article/page/2",
    #         "https://naked-science.ru/article/page/3",
    #         "https://naked-science.ru/article/page/4",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    async def parse(self, response, **kwargs):
        # page = "_".join(response.url.split("/")[2:])
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        for quote in response.css("div.news-item.grid"):
            title = quote.css("a::text").get()
            short_text = quote.css("p::text").get()
            published_at = quote.css("span::attr(data-published)").get()

            full_text_link = quote.css("a::attr(href)").get()
            full_text = await self.get_full_text(link=full_text_link)
            if not full_text:
                full_text = "Not available"

            tag = "science"  # или функция

            search_words: list = quote.css("div.terms-item a.animate-custom::text").getall()
            search_words_cleared: list = await self.clear_search_words(search_words)

            yield {"title": title,  # название
                   "brief_text": short_text,  # короткое описание
                   "full_text": full_text,  # полный текст
                   "tag": tag,  # тэг - одно слово
                   "search_words": search_words_cleared,  # слова для поиска
                   "full_text_link": full_text_link,  # ссылка на полный текст
                   "published_at": datetime.fromisoformat(published_at),  # дата публикации
                   "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                   }

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
