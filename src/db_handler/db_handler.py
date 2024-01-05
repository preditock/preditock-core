from config.conf import News, PS
import mysql.connector
import os
from dotenv import load_dotenv
from typing import Dict, Union, List, Tuple

dotenv_path = os.path.join(os.path.dirname(__file__), '../../config/data.env')

class Table:
    def __init__(self):
        load_dotenv(dotenv_path)
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('host'),
                database=os.getenv('database'),
                user=os.getenv('user'),
                password=os.getenv('password'),
                port=os.getenv('port')
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def insert(self):
        raise NotImplementedError("This method should be overridden in the child class")

    def get_all(self):
        raise NotImplementedError("This method should be overridden in the child class")

class NewsTable(Table):
    def insert(self, news_list: List[News]):
        query = """
        INSERT INTO news 
        (search_company, search_date, write_date, title, content, url, publisher, user_id, keyword, img_url, summary) 
        VALUES (%s, CURRENT_TIMESTAMP(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [(news.search_company, news.write_date, news.title, news.content, news.url, news.publisher, news.user_id, news.keyword, news.img_url, news.summary) for news in news_list]
        self.cursor.executemany(query, values)
        self.connection.commit()

    def get_news_by_id(self, news_id: str) -> Union[Dict[str, Union[str, int]], str]:
        query = "SELECT * FROM news_table WHERE `news_id` = %s"
        values = (news_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else "No data found for the given key."

    def get_all(self) -> List[Tuple]:
        query = "SELECT * FROM news_table"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if result else []

class PsTable(Table):
    def insert(self, ps: PS):
        query = """
        INSERT INTO ps 
        (news_id, company, score, user_id) 
        VALUES (%s, %s, %s, %s)
        """
        values = ps
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_all(self) -> List[Tuple]:
        query = "SELECT * FROM ps"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if result else []
