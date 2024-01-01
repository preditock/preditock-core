import mysql.connector
import os
from dotenv import load_dotenv

class Table:
    def __init__(self):
        load_dotenv('env/data.env')
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
        pass

    def get_all(self):
        pass

class NewsTable(Table):
    def insert(self, news):
        query = """
        INSERT INTO news 
        (search_company, search_date, write_date, title, content, url, img_url, publisher, keyword, summary, user_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = news
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_news_by_id(self, news_id):
        query = "SELECT * FROM news_table WHERE `news_id` = %s"
        values = (news_id)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else "No data found for the given key."

    def get_all(self):
        query = "SELECT * FROM news_table"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return {row[0]: row[1] for row in result} if result else {}

class PsTable(Table):
    def insert(self, ps):
        query = """
        INSERT INTO ps 
        (news_id, company, score, user_id) 
        VALUES (%s, %s, %s, %s)
        """
        values = ps
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_all(self):
        query = "SELECT * FROM ps"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result if result else []
