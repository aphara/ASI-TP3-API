#!flask/bin/python
from flask import Flask, jsonify
from model import article
import json
import jsonpickle
import mysql.connector as mariadb
import os
import config


app = Flask(__name__)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    mariadb_connection = mariadb.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'),
                                         database=os.environ.get('DB_NAME'))
    cur = mariadb_connection.cursor()
    cur.execute('''SELECT * FROM article WHERE article_id=1''')
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json_data
    #return jsonify({'tasks': results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
