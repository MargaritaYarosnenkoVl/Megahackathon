# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import asyncpg
import psycopg2

import scrapy
# useful for handling different item types with a single interface
from config import FSTR_DB_LOGIN, FSTR_DB_NAME, FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_PASS


class ParseNewsPipeline:

    def __init__(self):
        # connection details
        username = FSTR_DB_LOGIN
        password = FSTR_DB_PASS
        hostname = FSTR_DB_HOST
        port = FSTR_DB_PORT
        db_name = FSTR_DB_NAME

        self.connection = psycopg2.connect(user=username,
                                           password=password,
                                           host=hostname,
                                           port=port,
                                           dbname=db_name)

        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        self.cur.execute("""SELECT * FROM article WHERE title = %s""", (item['title'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            self.cur.execute(f"""
            INSERT INTO article (
            title, brief_text, full_text, tag, search_words, parsed_from, full_text_link, published_at, parsed_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (item.get('title'), item.get('brief_text'), item.get('full_text'), item.get('tag'),
                              item.get('search_words'), item.get('parsed_from'), item.get('full_text_link'),
                              item.get('published_at'), item.get('parsed_at')))
            self.connection.commit()
            print("\n" + item.get('title'), " --|---|-- is successfully added to table article! OK\n")
        return item

    def close_spider(self, spider: scrapy.Spider = None):  # , spider=None, reason=None
        self.cur.close()
        self.connection.close()
        print(spider)


class ParseTempNewsPipeline:

    def __init__(self):
        # connection details
        username = FSTR_DB_LOGIN
        password = FSTR_DB_PASS
        hostname = FSTR_DB_HOST
        port = FSTR_DB_PORT
        db_name = FSTR_DB_NAME

        self.connection = psycopg2.connect(user=username,
                                           password=password,
                                           host=hostname,
                                           port=port,
                                           dbname=db_name)

        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        username: str = getattr(spider, "username", "")
        self.cur.execute("""
        SELECT * FROM temp_article 
        WHERE (title = %s AND username = %s)""",
                         (item['title'], username))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            self.cur.execute("""
            INSERT INTO temp_article (
            title, brief_text, full_text, tag, search_words, parsed_from, 
            full_text_link, published_at, parsed_at, username
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (item.get('title'), item.get('brief_text'), item.get('full_text'), item.get('tag'),
                              item.get('search_words'), item.get('parsed_from'), item.get('full_text_link'),
                              item.get('published_at'), item.get('parsed_at'), username))
            self.connection.commit()
            print("\n" + item.get('title'), " --|---|-- is successfully added to table temp_article! OK\n")
        return item

    def close_spider(self, spider: scrapy.Spider = None):  # , spider=None, reason=None
        self.cur.close()
        self.connection.close()
