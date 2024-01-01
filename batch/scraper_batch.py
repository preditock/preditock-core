#run batch server

from scraper.scraper import NewsScraper

search_company = "삼성전자"

news_scrapper = NewsScraper()
result = news_scrapper.crawl_news(search_company, 1, 400)
with open("news_urls.txt", "a", encoding="utf-8") as file:
        file.write(str(result)+"\n")

