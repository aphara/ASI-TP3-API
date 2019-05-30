import mysql.connector as mariadb
import os
import config
from json import JSONEncoder
import json
from datetime import date


def test():
    mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), database=os.environ.get('DB_NAME'))
    cursor = mariadb_connection.cursor()
    results = []
    cursor.execute("SELECT author,title from article where author=\'Alex\'")
    for row in cursor.fetchall():
        results.append(row)
    return results


class Article(object):
    def __init__(self, id, author, title, date, section, status, text):
        self.id = id
        self.author = author
        self.title = title
        self.date = date
        self.section = section
        self.status = status
        self.text = text

    @classmethod
    def getAll(self):
        mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), database=os.environ.get('DB_NAME'))
        cursor = mariadb_connection.cursor()
        results = []
        cursor.execute("SELECT * from article")
        for row in cursor.fetchall():
            row = Article(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            results.append(row)
        return results

    @classmethod
    def getAlltoDict(self):
        mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), database=os.environ.get('DB_NAME'))
        cursor = mariadb_connection.cursor()
        articles = {}
        cursor.execute("SELECT * from article")
        for row in cursor.fetchall():
            articles['id': row[0]] = {'Author': row[1], 'Title': row[2], 'Date': row[3], 'Section': row[4]}
        return articles

    @staticmethod
    def insertdb(articles):
        try:
            mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), database=os.environ.get('DB_NAME'))
            cursor = mariadb_connection.cursor()
            sql_insert_query = """INSERT INTO article(author, title, date, section, status, text) 
            VALUES (%s,%s,%s,%s,%s,%s)"""
            cursor = mariadb_connection.cursor(prepared=True)
            result = cursor.executemany(sql_insert_query, articles)
            mariadb_connection.commit()
            return cursor.rowcount, "Record inserted successfully into python_users table"
        except mariadb.Error as error:
            return ("Failed to insert into MySQL table {}".format(error))
        finally:
            # closing database connection.
            if (mariadb_connection.is_connected()):
                cursor.close()
                mariadb_connection.close()
                return ("MySQL connection is closed")

    @staticmethod
    def getlastid():
        mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), database=os.environ.get('DB_NAME'))
        cursor = mariadb_connection.cursor()
        cursor.execute("SELECT article_id from article ORDER BY article_id DESC ")
        for row in cursor.fetchone():
            results = row
        return results

    def print(self):
        x = (self.author, self.title, self.date, self.section, self.status, self.text)
        return x

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ArticleEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Article):
            return object.__dict__

        if isinstance(object, date):
            return object.strftime('%Y-%m-%d')

        if isinstance(object, set):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)

