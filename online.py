import requests
import wikipedia
import pywhatkit as kit  # used to access google/ u tube
from email.message import EmailMessage
import smtplib  #inbuilt library used for simple mail transfer protocols
from decouple import config

EMAIL = "vinitkumar2105@gmail.com"
PASSWORD = "twdg fxjf jomk yuhh"


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(
        query)  #open any application online and perform actions this kit is part of pywhatkit module and search is function performing on google


def youtube(video):
    kit.playonyt(video)


def send_email(reciever_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = reciever_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey"
                          f"=93cd79f7e79b4e629c5a0e8a1820b5bd").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]

def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=37d56057d32dd41e703769cbda2ed136"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather,f"{temp}°C",f"{feels_like}°C"
