import mysql.connector as mariadb
import os
import config
from json import JSONEncoder
import json
from datetime import date


class Article(object):
    def __init__(self, id, author, title, date, section, status, text):
        self.id = id
        self.author = author
        self.title = title
        self.date = date
        self.section = section
        self.status = status
        self.text = text

    @staticmethod
    def getAlltoDict(Section):
        try:
            mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
                                                 database=os.environ.get('DB_NAME'), use_pure=True)
            cur = mariadb_connection.cursor(prepared=True)
            query = "SELECT * FROM article WHERE section=%s"
            cur.execute(query, (Section,))
            row_headers = [x[0] for x in cur.description]  # this will extract row headers
            rv = cur.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            return json_data
        except mariadb.Error as error:
            return ("Failed to select into MySQL table {}".format(error))
        finally:
            # closing database connection.
            if (mariadb_connection.is_connected()):
                cur.close()
                mariadb_connection.close()
                print("MySQL connection is closed")


class ArticleEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Article):
            return object.__dict__

        if isinstance(object, date):
            return object.strftime('%Y-%m-%d')

        if isinstance(object, set):
            return list(object)
        else:
            return json.JSONEncoder.default(self, object)

