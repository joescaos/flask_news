from flask import Flask, render_template, request
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

@app.route('/', methods=['GET', 'POST'])
@app.route('/<publication>')
def get_news(publication='bbc'):
    #query = request.args.get("publication")
    query = request.form.get("publication")
    app.logger.debug(query)
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']
    return  render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(port=5000, debug=True)