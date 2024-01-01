# 필요한 라이브러리를 불러옵니다.
from bs4 import BeautifulSoup
import requests
import re
import datetime

d = datetime.datetime.now()

class NewsScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
        self.news_data = []

    def makePgNum(self, num):
        if num == 1:
            return num
        elif num == 0:
            return num+1
        else:
            return num+9*(num-1)

    def makeUrl(self, search, start_pg, end_pg):
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = self.makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sort=1&start=" + str(page)
            urls.append(url)
        return urls    

    def news_attrs_crawler(self, articles, attrs):
        attrs_content = []
        for i in articles:
            attrs_content.append(i.attrs[attrs])
        return attrs_content

    def articles_crawler(self, url):
        original_html = requests.get(url, headers=self.headers)
        html = BeautifulSoup(original_html.text, "html.parser")
        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        url = self.news_attrs_crawler(url_naver, 'href')
        return url

    def makeList(self, newlist, content):
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist

    def crawl_news(self, search, start_pg, end_pg):
        urls = self.makeUrl(search, start_pg, end_pg)
        print(urls)
        news_url = []
        for url in urls:
            url = self.articles_crawler(url)
            news_url.append(url)
        
        news_url_1 = []
        self.makeList(news_url_1, news_url)

        print(news_url_1)

        final_urls = [url for url in news_url_1 if "news.naver.com" in url]

        for url in final_urls:
            news = requests.get(url, headers=self.headers)
            news_html = BeautifulSoup(news.text, "html.parser")
            title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
            if title == None:
                title = news_html.select_one("#content > div.end_ct > div > h2")


            try:
                span = news_html.find("span", class_="end_photo_org")
                if span is not None and span.img is not None:
                    news_image = span.img.get('data-src') 
                else:
                    news_image = None  
            except AttributeError:  
                news_image = None  

            content = news_html.select("article#dic_area")
            if content == []:
                content = news_html.select("#articeBody")

            pattern1 = '<[^>]*>'
            pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""

            title = re.sub(pattern1, '', str(title))
            content = re.sub(pattern1, '', ''.join(str(content)))
            content = content.replace(pattern2, '')

            try:
                html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
                news_date = html_date.attrs['data-date-time']
            except AttributeError:
                news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
                news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))

            news_info = {
                'title': title,
                'url': url,
                'news_image': news_image,
                'content': content,
                'date': news_date
            }
            self.news_data.append(news_info)

        return self.news_data

