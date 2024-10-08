import time
from random import choice
import wolframalpha
import pyttsx3  # Text-to-speech
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import pyautogui
import webbrowser
from datetime import datetime
from decouple import config  # Manage environment variables
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

# Define random responses
random_text = [
    "Cool, I'm on it",
    "Okay sir, I'm working on it",
    "Just a second sir"
]

# Initialize the speech engine
engine = pyttsx3.init('sapi5')  # SAPI5 for Windows
engine.setProperty('volume', 1.0)  # Set volume to 1.0
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female

# Load user and bot names from environment variables
USER = config('USER')
HOSTNAME = config('BOT')  # Ensure these are defined in your .env file

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {USER}")
    elif 16 <= hour < 21:
        speak(f"Good evening {USER}")
    speak(f"Hi {USER}, I am {HOSTNAME}. How can I help you?")

listening = False

def start_listening():
    global listening
    listening = True
    print("started listening")

def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k' , start_listening)
keyboard.add_hotkey('ctrl+alt+p' , pause_listening)


def take_command():
    r = sr.Recognizer()  # Use Google audio recognition API
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        queri = r.recognize_google(audio, language='en-in')
        print(f"User said: {queri}")
        if 'stop' not in queri and 'exit' not in queri:
            speak(choice(random_text))  # Use the list here
        else:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Good night sir, take care")
            else:
                speak("Have a good day")
            exit()
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        speak("Sorry, I couldn't understand. Can you please repeat that?")
        queri = 'None'
    return queri

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query or "how r u" in query:  # Fixed condition
                speak(f"I'm absolutely fine. What about you {USER}?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera")
                sp.run('start microsoft.windows.camera:',shell = True)


            elif "open notepad" in query:
                speak("Opening notepad for you")
                notepad_path = "C:\\Users\\vinit\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                os.startfile(notepad_path)


            elif "open blender" in query:
                speak("opening blender")
                blender_path = "C:\\Users\\vinit\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\blender\\Blender 4.2.lnk"
                os.startfile(blender_path)


            elif "open spotify" in query:
                speak("Opening Spotify, be ready to listen to music")
                spotify_path = "C:\\Program Files\\WindowsApps\\SpotifyAB.SpotifyMusic_1.247.366.0_x64__zpdnekdrzrea0\\Spotify.exe"
                os.startfile(spotify_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"your ip address is {ip_address}")
                print(f"your ip address is {ip_address}")

            elif "open youtube" in query:
                speak("what you want to play on youtube?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia, {results}")
                speak("I am printing this information on wikipedia")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send an email? Enter in the terminal")
                reciever_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message?")
                message = take_command().capitalize()
                if send_email(reciever_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep="\n")

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("Tell me name of your city")
                city = input("Enter name of your city:")
                speak(f"Getting weather report of {city} ")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp} but feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("I am printing this information on screen")
                print(f"Description: {weather}\nTemprature: {temp}\nFeels like: {feels_like}")


            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for " + text)
                speak("I found these")
                for movie in movies:
                    title = movie['title']
                    year = movie['year']
                    speak(f"{title}--{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info.get('rating', 'N/A')
                    cast = movie_info.get('cast', 'N/A')
                    actor = ', '.join(str(a) for a in cast[:5])
                    plot = movie_info.get('plot outline', 'Plot summary not available')
                    speak(f"{title} was released on {year} has IMDb ratings of {rating}. It has a cast of {actor}. The plot summary of the movie is {plot}")
                    print(f"{title} was released on {year} has IMDb ratings of {rating}. It has a cast of {actor}. The plot summary of the movie is {plot}")

            elif "calculate" in query:
                app_id = "R7456P-LR7KJKL55V"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that . Please try again")

            elif 'what is' in query or 'who is' in query or 'which is' in query:
                app_id = "R7456P-LR7KJKL55V"
                client = wolframalpha.Client(app_id)
                try:

                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind + 2:]
                        res = client.query(" ".join(text))
                        ans = next(res.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I couldn't find that. Please try again.")
                except StopIteration:
                    speak("I couldn't find that. Please try again.")

            elif "subscribe" in query:
                speak("Everyone who are watching this video, Please subscribe to listen more")
                speak("Firstly open youtube")
                webbrowser.open("https://www.youtube.com/")
                speak("click on search bar")
                pyautogui.moveTo(600, 182, 1)
                pyautogui.click(x = 600, y = 182, clicks=1, interval=1, button='left')
                speak("Sidhu Moose wala")
                pyautogui.typewrite("Sidhu Moose wala",0.1)
                time.sleep(1)
                speak("please enter")
                pyautogui.press('enter')
                # pyautogui.moveTo(971, 314, 1)
                speak("Here you will see legend's channel")
                pyautogui.moveTo(1580, 415,1)
                speak("click here to subscribe")
                pyautogui.click(x=1580, y=415,clicks=1, interval=1, button='left')
                speak("and also dont forget to press the bell icon")

                pyautogui.moveTo(1580,415,1)
                pyautogui.click(x=1580, y=415, clicks=1, interval=1, button='left')
                speak("turn on all notifications")
                pyautogui.click(x=1590, y=474, clicks=1, interval=1, button='left')

            elif "levels by sidhu moose wala" in query:
                speak("Firstly open youtube")
                webbrowser.open("https://www.youtube.com/")
                speak("click on search bar")
                pyautogui.moveTo(600, 182, 1)
                pyautogui.click(x=600, y=182, clicks=1, interval=1, button='left')
                pyautogui.typewrite("levels by Sidhu Moose wala", 0.1)
                time.sleep(1)
                pyautogui.press('enter')
                speak("playing levels by sidhu moose wala")
                pyautogui.moveTo(665, 420, 1)
                pyautogui.click(x=665, y=420, clicks=1, interval=1, button='left')


