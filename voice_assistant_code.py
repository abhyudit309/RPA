import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import random
import cv2
import requests
from selenium import webdriver
import time
import wolframalpha
from bs4 import BeautifulSoup
from urllib.request import urlopen
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import pyjokes
from googlesearch import search


def unicode_to_ascii(text):
    normal_text = (text.replace('\\xe2\\x80\\x99', "'").
                   replace('\\xc3\\xa9', 'e').
                   replace('\\xe2\\x80\\x90', '-').
                   replace('\\xe2\\x80\\x91', '-').
                   replace('\\xe2\\x80\\x92', '-').
                   replace('\\xe2\\x80\\x93', '-').
                   replace('\\xe2\\x80\\x94', '-').
                   replace('\\xe2\\x80\\x94', '-').
                   replace('\\xe2\\x80\\x98', "'").
                   replace('\\xe2\\x80\\x9b', "'").
                   replace('\\xe2\\x80\\x9c', '"').
                   replace('\\xe2\\x80\\x9c', '"').
                   replace('\\xe2\\x80\\x9d', '"').
                   replace('\\xe2\\x80\\x9e', '"').
                   replace('\\xe2\\x80\\x9f', '"').
                   replace('\\xe2\\x80\\xa6', '...').
                   replace('\\xe2\\x80\\xb2', "'").
                   replace('\\xe2\\x80\\xb3', "'").
                   replace('\\xe2\\x80\\xb4', "'").
                   replace('\\xe2\\x80\\xb5', "'").
                   replace('\\xe2\\x80\\xb6', "'").
                   replace('\\xe2\\x80\\xb7', "'").
                   replace('\\xe2\\x81\\xba', "+").
                   replace('\\xe2\\x81\\xbb', "-").
                   replace('\\xe2\\x81\\xbc', "=").
                   replace('\\xe2\\x81\\xbd', "(").
                   replace('\\xe2\\x81\\xbe', ")"))

    return normal_text


class Person:
    name = ''

    def set_name(self, user_name):
        self.name = user_name


def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 180)
    engine.say(audio)
    engine.runAndWait()


def there_exists(terms):
    for term in terms:
        if term in query:
            return True


def wish_me():
    hr = int(datetime.datetime.now().hour)
    if 0 <= hr < 12:
        speak('Good Morning')

    elif 12 <= hr < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak('Hello. I am Alfred. Please tell me how may I help you')


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        user_query = r.recognize_google(audio, language='en-in')
        print('User said', user_query)

    except sr.UnknownValueError:
        speak('Pardon')
        return 'None'
    return user_query


def open_web_page(url):
    chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), )
    webbrowser.get('chrome').open(url)


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('me18b088@smail.iitm.ac.in', '7uac7Y?8')
    server.sendmail('me18b088@smail.iitm.ac.in', to, content)
    server.close()


def play_music():
    music_dir = 'C:\\Music'
    songs = os.listdir(music_dir)
    a = random.randint(0, len(songs) - 1)
    os.startfile(os.path.join(music_dir, songs[a]))


def take_photo(no_of_photos):
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    for j in range(no_of_photos):
        return_value, image = camera.read()
        r = random.randint(1, 200000000)
        cv2.imwrite('photo' + str(r) + '.png', image)
    del camera
    cv2.destroyAllWindows()


def tell_time():
    now = datetime.datetime.now()
    if now.hour >= 13:
        hour = now.hour - 12
        speak(f'The time is {hour} {now.minute} pm')
    elif now.hour == 12:
        speak(f'The time is {now.hour} {now.minute} pm')
    elif now.hour == 0:
        speak(f'The time is 12 {now.minute} a m')
    else:
        speak(f'The time is {now.hour} {now.minute} a m')


def tell_date():
    day = datetime.datetime.today().weekday()
    day_dict = {0: 'Monday', 1: 'Tuesday',
                2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday',
                6: 'Sunday'}
    day_of_the_week = day_dict[day]
    now = datetime.datetime.now()
    month_dict = {1: 'January', 2: 'February',
                  3: 'March', 4: 'April',
                  5: 'May', 6: 'June',
                  7: 'July', 8: 'August',
                  9: 'September', 10: 'October',
                  11: 'November', 12: 'December'}
    current_month = month_dict[now.month]
    speak(f"Today's date is {day_of_the_week} {now.day} {current_month} {now.year}")


def weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?appid=4068895124380499cdbec660d5c0c18b&q=" + city
    response = requests.get(url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        temperature = y["temp"]
        temperature_min = y["temp_min"]
        temperature_max = y["temp_max"]
        humidity_percent = y["humidity"]
        z = x["weather"]
        description_general = z[0]["description"]
        return temperature, temperature_min, temperature_max, humidity_percent, description_general
    else:
        pass


def send_whatsapp(name_person, message):
    driver = webdriver.Chrome(executable_path=r'C:\Users\Abhyudit\Downloads\chromedriver_win32\chromedriver.exe') # install chromedriver
    driver.get('https://web.whatsapp.com/')
    speak('say yes to scan QR code')
    said = take_command().lower()
    if 'yes' in said:
        time.sleep(5)
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name_person))
        user.click()
        msg_box = driver.find_element_by_class_name('_3uMse')
        msg_box.send_keys(message)
        button = driver.find_element_by_class_name('_1U1xa')
        button.click()
    else:
        pass


def news1():
    res = requests.get('https://www.indiatoday.in/')
    soup = BeautifulSoup(res.text, 'lxml')
    news_box = soup.find('ul', {'class': 'itg-listing'})
    all_news = news_box.find_all('a')
    for news in all_news:
        speak(news.text)


def news2():
    news_url = 'https://news.google.com/news/rss'
    client = urlopen(news_url)
    xml_page = client.read()
    client.close()
    soup_page = BeautifulSoup(xml_page, 'xml')
    news_list = soup_page.find_all('item')
    for news in news_list[:5]:
        speak(unicode_to_ascii(news.title.text))


def play_video(video_name):
    driver = webdriver.Chrome(executable_path=r'C:\Users\Abhyudit\Downloads\chromedriver_win32\chromedriver.exe') # install chromedriver
    url = 'https://www.youtube.com/results?q=' + video_name
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver.get(url)
    sc_text = driver.page_source
    driver.quit()
    soup = BeautifulSoup(sc_text, "html.parser")
    songs = soup.findAll("a", {"id": "video-title"})
    song = songs[0]
    song_url = song['href']
    webbrowser.open("https://www.youtube.com" + song_url)


def distance_bet_cities(city1, city2):
    api_key = '4db48d0600774c6da81cd2b17863fb08'
    geocoder = OpenCageGeocode(api_key)
    results1 = geocoder.geocode(city1)
    results2 = geocoder.geocode(city2)
    lat1 = results1[0]['geometry']['lat']
    lng1 = results1[0]['geometry']['lng']
    lat2 = results2[0]['geometry']['lat']
    lng2 = results2[0]['geometry']['lng']
    city1_coordinates = (lat1, lng1)
    city2_coordinates = (lat2, lng2)
    distance = round(geodesic(city1_coordinates, city2_coordinates).km, 2)
    speak(f'the aerial distance between {city1} and {city2} is {distance} kilometres')


def answer(question):
    app_id = '2JLH78-97XTV83778'
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    ans = next(res.results).text
    return ans


def calculate(problem):
    app_id = '2JLH78-97XTV83778'
    client = wolframalpha.Client(app_id)
    q = problem[problem.find('calculate'):].replace('calculate', '').strip()
    res = client.query(q)
    solution = next(res.results).text
    speak('The answer is ' + solution)


def google_search(keyword):
    j = search(keyword, tld='co.in', num=1, stop=1, pause=2)
    url = list(j)[0]
    open_web_page(url)


if __name__ == "__main__":

    person_obj = Person()
    hot_word = take_command().lower()
    if hot_word == 'hello alfred':
        wish_me()
        while True:
            query = take_command().lower()

            if there_exists(['tell me about', 'know about']) and 'yourself' not in query:
                item = query[query.find('about'):].replace('about', '').strip()
                results = wikipedia.summary(item, sentences=2)
                speak('According to wikipedia')
                print(results)
                speak(results)

            elif 'open google' in query:
                open_web_page('google.com')

            elif 'open whatsapp' in query:
                open_web_page('web.whatsapp.com')

            elif 'play music' in query:
                play_music()

            elif there_exists(["what's the date", 'tell me the date']):
                tell_date()

            elif there_exists(["what's the time", 'tell me the time', 'what time is it']):
                tell_time()

            elif 'open matlab' in query:
                codePath = "C:\\Program Files\\MATLAB\\R2019b\\bin\\matlab.exe"
                os.startfile(codePath)

            elif 'send' and 'email' in query:
                try:
                    if 'person1' in query:
                        speak('What should I send')
                        contents = take_command()
                        send_email('email_id1', contents)
                        speak('Email has been sent')

                    elif 'person2' in query:
                        speak('What should I send')
                        contents = take_command()
                        send_email('email_id2', contents)
                        speak('Email has been sent')

                    elif 'person3' in query:
                        speak('What should I send')
                        contents = take_command()
                        send_email('email_id3', contents)
                        speak('Email has been sent')

                    else:
                        speak('sender not in the list')

                except Exception as e:
                    print(e)
                    speak('Sorry I am not able to send the email')

            elif there_exists(['click a photo', 'take a photo', 'click a picture']):
                try:
                    # speak('how many photos should I take ?')
                    # no1 = int(take_command())
                    take_photo(1)
                    speak('the photo is taken')
                except Exception as e:
                    print(e)
                    speak('Sorry I am not able to understand')

            elif 'weather' in query:
                try:
                    speak("Which city's forecast do you want to know")
                    city_name = take_command()
                    temp, temp_min, temp_max, humidity, description = weather(city_name)
                    temp_c = str(round(temp - 273, 1))
                    temp_min_c = str(round(temp_min - 273, 1))
                    temp_max_c = str(round(temp_max - 273, 1))
                    speak(
                        'the temperature ranges from ' + temp_min_c + ' degree celsius to' + temp_max_c + 'degree '
                                                                                                          'celsius')
                    speak('the current temperature is ' + temp_c + ' degree celsius')
                    speak('the humidity is ' + str(humidity) + ' percent')
                    speak('the description is ' + description)
                except Exception as e:
                    print(e)
                    speak('Sorry I am not able to understand')

            elif 'whatsapp' and 'message' in query:
                try:
                    i = query.split().index('to')
                    name = query.split()[i + 1].title()
                    speak('What should I send')
                    msg = take_command().lower()
                    send_whatsapp(name, msg)
                    speak('Message sent')
                except Exception as e:
                    print(e)
                    speak('Sorry I am not able to send the message')

            elif there_exists(['tell me news', 'what is the breaking news', 'what is the news']):
                speak('from where do you want the news')
                news_name = take_command().lower()
                if 'india today' in news_name:
                    speak('These are the top stories for today')
                    news1()
                elif 'google' in news_name:
                    speak('These are the top stories for today')
                    news2()
                else:
                    speak('Sorry, unavailable')

            elif 'play' and 'youtube' in query:
                video_title = query[query.find('play'):].replace('play', '').replace('on youtube', '').strip()
                try:
                    play_video(video_title)
                except Exception as e:
                    print(e)
                    speak('Video not found')

            elif 'distance between' in query:
                city1_name = query.split()[-3]
                city2_name = query.split()[-1]
                distance_bet_cities(city1_name, city2_name)

            elif 'who is the' in query:
                try:
                    ask = query[query.find('who'):]
                    reply = answer(ask)
                    speak(ask.replace('who is', '').strip() + ' is ' + reply)
                except Exception as e:
                    print(e)
                    ask = query[query.find('who'):]
                    google_search(ask)

            elif 'what is the' in query and 'time' not in query:
                ask = query[query.find('what'):]
                reply = answer(ask)
                speak(ask.replace('what is', '').strip() + ' is ' + reply)

            elif 'tell me a joke' in query:
                speak(pyjokes.get_joke())

            elif 'write a note' in query:
                speak('What should i write')
                note = take_command()
                file = open('jarvis.txt', 'w')
                speak('Should i include date and time')
                rep = take_command()
                if 'yes' in rep:
                    strTime = datetime.datetime.now().strftime("% H:% M:% S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)

            elif 'calculate' in query:
                calculate(query)

            elif 'tell me about yourself' in query:
                speak('''My name is Alfred. I'm your personal voice assistant.
                      I can do many things like sending emails, clicking photographs,
                      sending whatsapp messages, answering general questions, 
                      telling you the news, tell you about the weather,
                      play videos and music for you, and whatnot''')

            elif 'google search' in query:
                word = query[query.find('google'):].replace('google search', '').strip()
                google_search(word)

            elif 'how are you' in query:
                speak(f"I'm very well. Thanks for asking {person_obj.name}")

            elif 'my name is' in query:
                person_name = query.split()[-1]
                speak(f'Okay, I will remember that {person_name}')
                person_obj.set_name(person_name)

            elif there_exists(['what is your name', "what's your name", 'tell me your name']):
                if person_obj.name:
                    speak('My name is Alfred')
                else:
                    speak("My name is Alfred. What's your name?")

            elif there_exists(['thank you', 'bye', 'goodbye']):
                speak(f'You are welcome. Goodbye and see you soon {person_obj.name}')
                exit()
