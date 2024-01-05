import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.conf import News
from src.scraper.scraper import NewsScraper
from src.db_handler.db_handler import NewsTable
from typing import List

def crawl_news(search: str, start_pg: int, end_pg: int) -> List[News]:
    scraper = NewsScraper()
    urls = scraper.make_url(search, start_pg, end_pg)
    final_urls = scraper.process_urls(urls)

    return [scraper.process_each_url(url) for url in final_urls]

def save_news_to_db(company: str, page_start: int, page_end: int):
    news_list = crawl_news(company, page_start, page_end)
    
    news_table = NewsTable()

    for news in news_list:
        news_table.insert(news)


if __name__ == "__main__":
    save_news_to_db("삼성전자", 100, 200)
