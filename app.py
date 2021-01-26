from flask import Flask, render_template, request, make_response
import feedparser
import json
import datetime
import urllib.request,urllib.parse, urllib.error
import requests
from secrets import WEATHER_API_KEY, CURRENCY_APY_KEY


app = Flask(__name__)


RSS_FEEDS =  {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS = {
    'publication': 'bbc',
    'city': 'Bogota',
    'currency_from': 'USD',
    'currency_to': 'COP'
}

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
    #print(city)
    # 1. get the api url with the api key
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}"
    # 2. fetching the api url
    url = urllib.request.urlopen(api_url)
    #print(url)
    # 3. read the http response
    data = url.read()
    #print(data)
    # 4. convert the response to json
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {"description":
                    parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"],
                    "country": parsed['sys']['country']
                    }
    #print(weather)
    return weather

def get_rate(frm, to):
    currency_url = f"https://openexchangerates.org//api/latest.json?app_id={CURRENCY_APY_KEY}"
    data = urllib.request.urlopen(currency_url).read()
    data = json.loads(data).get('rates')
    frm_rate = data.get(frm.upper())
    to_rate = data.get(to.upper())
    return (to_rate/frm_rate, data.keys())

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@app.route('/', methods=['GET', 'POST'])
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    city = get_value_with_fallback("city")
    city = city.replace(' ', '+')
    weather = get_weather(city)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template('index.html',
                                articles=articles, 
                                weather=weather,
                                currency_from=currency_from,
                                currency_to=currency_to,
                                rate=rate,
                                currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return  response


if __name__ == '__main__':
    app.run(port=5000, debug=True)