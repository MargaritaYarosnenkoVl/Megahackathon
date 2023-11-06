from pathlib import Path
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp
import scrapy


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
            full_text_link = quote.css("a::attr(href)").get()
            full_text = await self.get_full_text(link=full_text_link)
            if not full_text:
                full_text = "Not available"

            yield {"title": title,
                   "short_text": short_text,
                   "full_text": full_text,
                   "link": full_text_link}

    async def get_full_text(self, link: str) -> str:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            post_lead: str = soup.find('div', {"class": "post-lead"}).text
            paragraphs = soup.find('div', {"class": "body"}).findAll("p")
            full_t = post_lead.strip() + " " + " ".join((p.text.strip() for p in paragraphs))
            return full_t
