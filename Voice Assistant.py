import pyjokes as pyjokes
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import pyaudio
import headlines
import getpass
import librosa
import soundfile
import numpy as np
import os, pickle,glob
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pickle
from scipy.io import wavfile

pyttsx3.speak("Enter your password")
inpass = getpass.getpass("Enter your password :")
apass = "ashwin"
if inpass != apass:
    pyttsx3.speak("Incorrect Password Try Again ")
    exit()
pyttsx3.speak("Access Granted")


print("Loading your AI personal assistant - Ashtech ")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")



def take_First_Command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        with open("audio_file.wav", "wb") as file:
            file.write(audio.get_wav_data())
        user_mood()

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


def user_mood():
    with soundfile.SoundFile('audio_file.wav') as s_file:
        x = s_file.read(dtype="float32")
        sample_rate = s_file.samplerate
    # x,sample_rate=soundfile.read(s_file)
        chroma=True
        mfcc=True
        mel=True
        if chroma:
            stft=np.abs(librosa.stft(x))
        result=np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=x, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(x, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))

    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
        result=np.array(result)
        result=result.reshape(180,1)
        result=result.transpose()
        pred=model.predict(result)
        if(pred==1):
            speak('You seem happy today')
            print('You seem happy today :)')

        elif(pred==0):
            speak(' Should I tell you some jokes to make your mood before')
            print('Should I tell you some jokes to make your mood before')
            statement1 = takeCommand().lower()
            if 'yes' in statement1:
                joke = pyjokes.get_joke('en', 'all')
                print(joke)
                speak(joke)
            else:
                return



speak("Loading your AI personal assistant AshTech")
wishMe()


if __name__ == '__main__':

    statement = take_First_Command().lower()
    while True:


        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement or "quit" in statement or "close" in statement:
            print('your personal assistant Ashtech is shutting down, Good bye')
            speak('your personal assistant Ashtech  is shutting down, Good bye')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'covid-19 tracker' in statement:
            webbrowser.open_new_tab(
                "https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen")
            speak("covid-19 tracker is open now")
            time.sleep(5)

        elif "shoping" in statement or 'shopping' in statement:
            websites = ['amazon', 'flipkart', 'myntra', 'limeroad']
            print('\n'.join(websites))
            speak("nice mood sir!, what do you want to open?")
            user_ip = takeCommand().lower().replace(' ', '')

            for website in websites:
                if website in user_ip:
                    webbrowser.open(website + '.com')

            speak("here you are sir")

        elif 'online courses' in statement or 'course' in statement:
            platforms = ['coursera', 'udemy', 'edx',
                         'skillshare', 'datacamp', 'udacity']
            speak("Select a platform that you prefer : ")
            print("\n".join(platforms))
            statement1 = takeCommand().lower()
            if statement1 == 0:
                continue
            if 'coursera' in statement1:
                webbrowser.open_new_tab("https://www.coursera.org")
                speak("Coursera is open now")
                time.sleep(2)
            elif 'udemy' in statement1:
                webbrowser.open_new_tab("https://www.udemy.com")
                speak("udemy is open now")
                time.sleep(2)
            elif 'edx' in statement1:
                webbrowser.open_new_tab("https://www.edx.org/")
                speak("edx is open now")
                time.sleep(2)
            elif 'skillshare' in statement1:
                webbrowser.open_new_tab("https://www.skillshare.com")
                speak("skill share is open now")
                time.sleep(2)
            elif 'datacamp' in statement1:
                webbrowser.open_new_tab("https://www.datacamp.com")
                speak("datacamp is open now")
                time.sleep(2)
            elif 'udacity' in statement1:
                webbrowser.open_new_tab("https://www.udacity.com")
                speak("udacity is open now")
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)
        
        elif 'jobs' in statement or 'job' in statement or 'job recommandation' in statement or 'work' in statement:
            platforms = ['linkedin', 'indeed', 'glassdoor', 'hackerrank', 'naukri', 'intern shala']
            speak("Select a platform that you prefer:")
            print('\n'.join(platforms))
            statement1 = takeCommand().lower()
            if(statement1 == 0):
                continue
            if 'LinkedIn' in statement1:
                webbrowser.open_new_tab("https://www.linkedin.com/jobs")
                speak("LinkedIn is open now")
                time.sleep(2)
            elif 'Indeed' in statement1:
                webbrowser.open_new_tab("https://www.indeed.com/jobs")
                speak("Indeed is open now")
                time.sleep(2)
            elif 'Glassdoor' in statement1:
                webbrowser.open_new_tab("https://www.glassdoor.com/jobs")
                speak("Glassdoor is open now")
                time.sleep(2)
            elif 'HackerRank' in statement1:
                webbrowser.open_new_tab("https://www.hackerrank.com/jobs/search")
                speak("HackerRank is open now")
                time.sleep(2)
            elif 'Naukri' in statement1:
                webbrowser.open_new_tab("https://www.naukri.com/jobs")
                speak("Naukri is open now")
                time.sleep(2)
            elif 'intern shala' in statement:
                webbrowser.open_new_tab('internshala.com')
                speak('Intern Shala is open now')
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)
        
        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                speak(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Ashwin friend Ashtech version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather'
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Ashwin Kumar Ramaswamy")
            print("I was built by Ashwin Kumar Ramaswamy")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab(
                "https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            speak(
                'If you like the headline, say "visit" to open the page and read details')
            headlines = headlines.get_headlines(
                "https://timesofindia.indiatimes.com/home/headlines")
            for i in range(15):
                speak(headlines['text'][i])
                command = takeCommand()
                if 'visit' in command:
                    webbrowser.open_new_tab(headlines['link'][i])
                    break
                elif 'stop' in command:
                    break
                time.sleep(5)
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

            
        elif 'jokes' in statement or 'joke' in statement:
            joke = pyjokes.get_joke('en', 'all')
            print(joke)
            speak(joke)

        elif 'pycharm' in statement or 'open pycharm' in statement:
            os.startfile('pycharm')
            speak("pycharm is open now")



        elif 'what is my current location' in statement or 'what is my location' in statement or 'where am I' in statement:
            ip = "https://api.ipify.org/"
            ip_r = requests.get(ip).text
            
            geoip = "http://ip-api.com/json/"+ip_r
            geo_r = requests.get(geoip)
            geo_json = geo_r.json()

            print(f"Your current location is {geo_json['city']}, {geo_json['regionName']}, {geo_json['country']} {geo_json['zip']}")
            speak(f"Your current location is {geo_json['city']}, {geo_json['regionName']}, {geo_json['country']} {geo_json['zip']}")

        elif "notepad" in statement:
            speak("Opening Notepad")
            os.system("start Notepad")

        elif "outlook" in statement:
            speak("Opening Microsoft Outlook")
            os.system("start outlook")

        elif "word" in statement:
            speak("Opening Word")
            os.system("start winword")

        elif "paint" in statement:
            speak("Opening Paint")
            os.system("start mspaint")

        elif "excel" in statement:
            speak("Opening Excel")
            os.system("start excel")

        elif "chrome" in statement:
            speak("Opening Google Chrome")
            os.system("start chrome")

        elif "power point" in statement or "powerpoint" in statement or "ppt" in statement:
            speak("Opening Notepad")
            os.system("start powerpnt")

        elif "edge" in statement:
            speak("Opening Microsoft Edge")
            os.system("start msedge")

        elif "snipping tool" in statement:
            speak("Opening Snipping Tool")
            os.system("start snippingtool")

        elif "calculator" in statement:
            speak("Opening Calculator")
            os.system("start calc")

        elif "log off" in statement or "sign out" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()

time.sleep(3)
