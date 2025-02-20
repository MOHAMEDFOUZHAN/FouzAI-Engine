import requests
import pyttsx3
import time
from datetime import datetime, timedelta
import subprocess
import wikipedia
import pywhatkit as kit
import pyautogui
import json
import geocoder
import pyaudio
import psutil



# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Function to make the assistant speak and write (print)
def speak_and_write(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Function to wish the user
def wish_user():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        speak_and_write("Good morning,Fouzhan!")
    elif 12 <= hour < 17:
        speak_and_write("Good afternoon,Fouzhan!")
    elif 17 <= hour < 21:
        speak_and_write("Good evening,Fouzhan!")
    else:
        speak_and_write("Sir,this is your bedtime")

# Get current weather with additional details
def get_weather():
    city = "coimbatore"
    api_key = ""  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            speak_and_write(f"The current temperature in {city} is {temperature}°C with {weather_description}.")
            speak_and_write(f"Humidity is {humidity}% and wind speed is {wind_speed} m/s.")
        else:
            speak_and_write("Sorry, I couldn't fetch the weather data.")
    except Exception as e:
        speak_and_write(f"Error fetching weather data: {e}")

# Function to get and announce the user's current location
def get_location():
    try:
        g = geocoder.ip('me')  # Get location based on the IP address
        city = g.city
        region = g.state
        country = g.country
        if city and region and country:
            location = f"You are currently in {city}, {region}, {country}."
            speak_and_write(location)
        else:
            speak_and_write("Sorry, I couldn't determine your exact location.")
    except Exception as e:
        speak_and_write(f"Error fetching location: {e}")

# Show current time and date
def show_time():
    wish_user()
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    day_of_week = now.strftime("%A")
    speak_and_write(f"Today is {day_of_week}. The current time is {current_time}.")
show_time()
get_weather()

# Function to open applications
def open_chrome():
    speak_and_write("Opening Chrome...")
    subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

def open_notepad():
    speak_and_write("Opening Notepad...")
    subprocess.Popen(['notepad.exe'])

def open_edge():
    speak_and_write("Opening Edge...")
    subprocess.Popen(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

def open_instagram():
    speak_and_write("Opening Instagram...")
    url = "https://www.instagram.com"
    subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", url])

# Wikipedia search
def searching_wikipedia(ch):
    speak_and_write("Searching in Wikipedia...")
    try:
        ch = ch.replace("wikipedia", "").strip()
        result = wikipedia.summary(ch, sentences=2)
        speak_and_write("According to Wikipedia:")
        speak_and_write(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak_and_write(f"Multiple results found: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak_and_write("The Wikipedia service timed out, please try again later.")
    except Exception as e:
        speak_and_write(f"Sorry, I couldn't find any results on Wikipedia. Error: {e}")

# Function to record audio
def record_audio(duration=5, rate=44100, channels=1, frames_per_buffer=1024):
    # Initialize the audio stream
    p = pyaudio.PyAudio()

    # Open a stream to capture audio from the default microphone
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate,
                    input=True, frames_per_buffer=frames_per_buffer)

    print("Recording...")

    # Record audio for the given duration (in seconds)
    frames = []
    for _ in range(0, int(rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    print("Recording finished")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Return the recorded audio frames
    return frames


def send_whatsapp_message():
    # Get user input
    phone_number = input("Enter the phone number (with country code, e.g., +91XXXXXXXXXX): ")
    message = input("Enter the message to send: ")

    print("Enter the time to send the message:")
    send_hour = int(input("Hour (24-hour format): "))
    send_minute = int(input("Minute: "))

    try:
        # Schedule the WhatsApp message
        kit.sendwhatmsg(phone_number, message, send_hour, send_minute, wait_time=15)
        print("Message scheduled successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


# Add Search Capabilities (Google, YouTube, etc.)
def search_google(query):
    kit.search(query)
    speak_and_write(f"Searching Google for {query}")

def search_youtube(query):
    kit.playonyt(query)
    speak_and_write(f"Searching YouTube for {query}")

# Reminder management
def save_reminders(reminders):
    with open("reminders.json", "w") as file:
        json.dump(reminders, file, indent=4)

def load_reminders():
    try:
        with open("reminders.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []



def add_reminder(title, date, time):
    reminders = load_reminders()
    reminder_time = f"{date} {time}"
    reminders.append({"title": title, "time": reminder_time})
    save_reminders(reminders)
    speak_and_write(f"Reminder '{title}' set for {reminder_time}.")

def check_reminders():
    reminders = load_reminders()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    updated_reminders = []

    for reminder in reminders:
        if reminder["time"] == current_time:
            speak_and_write(f"Reminder: {reminder['title']}")
        elif datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M") > datetime.now():
            updated_reminders.append(reminder)

    save_reminders(updated_reminders)

def about_me():
    speak_and_write("I am created by Fouzhan. I am a personal AI assistant for Fouzhan.")

def about_owner():
    speak_and_write("""Hello, Fouzhan! You're a passionate learner, focusing on full-stack development and AI. You're
                  working on various projects, including a smart farming AI system and an environmental
                    monitoring system. You’re also involved in freelancing, specifically with social media post
                    design, and you’ve recently started learning illustration.
                    enjoy experimenting with new technologies like Python, Adobe Premiere Pro, and Blender.
                    You've also been involved in several hackathons and have a strong interest in robotics and AI. """)

# Get news headlines using the News API
def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=d95b801c61324ae0af316a27e9b923f8"
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        news_data = response.json()

        if 'articles' in news_data:
            headlines = [article['title'] for article in news_data['articles']]
            return headlines[:5]  # Return the top 5 headlines
        else:
            return "No articles found in the response."

    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {e}"

# Command handler to get the news
def handle_news():
    headlines = get_news()
    if isinstance(headlines, list):
        speak_and_write("Here are the top news headlines:")
        for i, headline in enumerate(headlines, 1):
            speak_and_write(f"{i}. {headline}")
    else:
        speak_and_write(headlines)

# Main user command handler
def main_handler():
    speak_and_write("hello Fouzhan....")
    while True:
        command = input("Enter your command: ").lower()
        
        # Command handling
        if "chrome" in command:
            open_chrome()
        elif "notepad" in command:
            open_notepad()
        elif "edge" in command:
            open_edge()
        elif "instagram" in command:
            open_instagram()
        elif "time" in command:
            show_time()
        elif "weather" in command:
            get_weather()
        elif "location" in command or "my location" in command or "where am i" in command or "where i am" in command:
            get_location()
        elif "wikipedia" in command:
            query = command.split("wikipedia", 1)[1].strip()
            searching_wikipedia(query)
        elif "reminder" in command:
            title, date, time = command.split(" ", 3)
            add_reminder(title, date, time)
        elif "check reminder" in command:
            check_reminders()
        elif "news" in command:
            handle_news()
        elif "about you" in command:
            about_me()
        elif "about owner" in command:
            about_owner()
        elif "serach in chrome" in command or "search in google":
            query=input("enter what to sreach:")
            search_youtube(query)
        elif "serach in youtube" in command:
            query=input("enter what to sreach:")
            search_youtube(query)
        elif "send message" in command:
            send_whatsapp_message()
        elif "record the audio" in command:
            record_audio()
        
        else:
            speak_and_write("Sorry, I didn't understand that command.")
if __name__ == "__main__":
    main_handler()  # Call the main command handler
