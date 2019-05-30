#!flask/bin/python
from flask import Flask
from model import article


app = Flask(__name__)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    json_data = article.Article.getAlltoDict("Music")
    return article.ArticleEncoder().encode(json_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
