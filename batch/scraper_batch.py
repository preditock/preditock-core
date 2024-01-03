import os
import sys
from dotenv import load_dotenv
from env.conf import News
from scraper.scraper import NewsScraper
from db_handler.db_handler import NewsTable
from typing import List

load_dotenv('env/data.env')
sys.path.insert(0, os.getenv('device_path'))

def crawl_news(search: str, start_pg: int, end_pg: int) -> List[News]:
    scraper = NewsScraper()
    urls = scraper.makeUrl(search, start_pg, end_pg)
    final_urls = scraper.process_urls(urls)

    return [scraper.process_each_url(url) for url in final_urls]

def save_news_to_db(company: str, page_start: int, page_end: int):
    news_list = crawl_news(company, page_start, page_end)
    
    news_table = NewsTable()

    for news in news_list:
        news_table.insert(news)


save_news_to_db("삼성전자", 1, 400)
