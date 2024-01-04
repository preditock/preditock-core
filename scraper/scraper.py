from bs4 import BeautifulSoup
import requests
import re
from typing import List
from datetime import datetime

from config.conf import News

class NewsScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
        self.search_company = None 

    def makePgNum(self, num: int) -> int:
        if num == 1:
            return num
        elif num == 0:
            return num+1
        else:
            return num+9*(num-1)

    def makeUrl(self, search: str, start_pg: int, end_pg: int) -> List[str]:
        self.search_company = search 
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = self.makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sort=1&start=" + str(page)
            urls.append(url)
        return urls  

    def news_attrs_crawler(self, articles: List[str], attrs: str) -> List[str]:
        attrs_content = []
        for i in articles:
            attrs_content.append(i.attrs[attrs])
        return attrs_content

    def articles_crawler(self, url: str) -> List[str]:
        original_html = requests.get(url, headers=self.headers)
        html = BeautifulSoup(original_html.text, "html.parser")
        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        url = self.news_attrs_crawler(url_naver, 'href')
        return url

    def makeList(self, newlist: List[str], content: List[str]) -> List[str]:
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist
    
    def process_urls(self, urls: List[str]) -> List[str]:
        news_url = []
        for url in urls:
            url = self.articles_crawler(url)
            news_url.append(url)

        news_url_1 = []
        self.makeList(news_url_1, news_url)

        print(news_url_1)

        final_urls = [url for url in news_url_1 if "news.naver.com" in url and "sports" not in url]
        
        return final_urls
    
    def process_each_url(self, url: str) -> News:
        news = requests.get(url, headers=self.headers)
        news_html = BeautifulSoup(news.text, "html.parser")
        
        # 제목 추출
        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")

        # 이미지 추출
        try:
            span = news_html.find("span", class_="end_photo_org")
            if span is not None and span.img is not None:
                news_image = span.img.get('data-src') 
            else:
                news_image = None  
        except AttributeError:  
            news_image = None  

        # 내용 추출
        content = news_html.select("article#dic_area")
        if content == []:
            content = news_html.select("#articeBody")

        # 언론사 정보 추출
        try:
            publisher = news_html.select_one("span._sp_each_source").text
        except AttributeError:
            publisher = "empty"

        try:
            html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern='<[^>]*>', repl='', string=str(news_date))

        if not news_date:
            news_date = '0000-00-00 00:00:00'
        else:
            try:
                news_date = datetime.strptime(news_date, '%Y-%m-%d %H:%M:%S')  
            except ValueError:
                news_date = '0000-00-00 00:00:00'

        # 불필요한 태그 제거
        pattern1 = '<[^>]*>'
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        title = re.sub(pattern1, '', str(title))
        content = re.sub(pattern1, '', ''.join(str(content)))
        content = content.replace(pattern2, '')

        # News 객체 생성
        news_info = News(
            search_company=self.search_company, 
            write_date=news_date,
            title=title,
            content=content,
            url=url,
            img_url=news_image,
            publisher=publisher,  # 언론사 정보 추가
            keyword=None,  
            summary=None,  
            user_id=None  
        )

        return news_info

