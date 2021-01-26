from flask import Flask, render_template, request
import feedparser
import json
import urllib.request,urllib.parse, urllib.error
import requests


app = Flask(__name__)
API_KEY = "da0f78399d23003917b1e6e2a068e212"

RSS_FEEDS =  {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    'publication': 'bbc',
    'city': 'Bogota'
}

@app.route('/', methods=['GET', 'POST'])
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    city = city.replace(' ', '+')
    weather = get_weather(city)
    return  render_template('index.html', articles=articles, weather=weather)

def get_news(query):
    #query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']
    return articles
    

def get_weather(city):
    query = urllib.parse.quote(city)
    print(city)
    # 1. get the api url with the api key
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    # 2. fetching the api url
    url = urllib.request.urlopen(api_url)
    print(url)
    # 3. read the http response
    data = url.read()
    print(data)
    # 4. convert the response to json
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {"description":
                    parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"]
                    }
    #print(weather)
    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)