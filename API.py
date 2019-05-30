#!flask/bin/python
from flask import Flask
from model import article


app = Flask(__name__)


@app.route('/api/articles/<string:section>', methods=['GET'])
def get_articles(section):
    json_data = article.Article.getAlltoDict(section)
    return article.ArticleEncoder().encode(json_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
