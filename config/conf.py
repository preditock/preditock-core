from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class News:
    search_company: str 
    write_date: str
    title: str
    content: List[str]
    url: str
    publisher: str
    keyword: List[str]
    img_url: Optional[str] = None
    summary: str = None
    user_id: Union[str, int] = None

@dataclass
class PS:
    news_id: str
    company: str
    score: str
    user_id: str
