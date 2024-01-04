from collections import namedtuple

# 뉴스 데이터 모델 정의
News = namedtuple('News', ['search_company', 'write_date', 'title', 'content', 'url', 'img_url', 'publisher', 'keyword', 'summary', 'user_id'])

# Ps 데이터 모델 정의
PS = namedtuple('PS', ['news_id', 'company', 'score', 'user_id'])