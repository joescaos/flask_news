from flask import Flask, render_template
import feedparser

app = Flask(__name__)

RSS_FEEDS =  {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}


def bbc():
    return get_news('bbc')

def cnn():
    return get_news('cnn')

@app.route('/')
@app.route('/<publication>')
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    title = first_article.get('title')
    #print(first_article)
    published = first_article.get('published')
    summary = first_article.get('summary')
    return  """<html>
                    <body>
                        <h1> BBC Headlines </h1>
                        <b>{0}</b> <br/>
                        <i>{1}</i> <br/>
                        <p>{2}</p> <br/>
                    </body>
                </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)