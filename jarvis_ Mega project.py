import speech_recognition  as sr 
import webbrowser
import pyttsx3   
import musiclibrary   
import difflib
import requests 
import datetime
import socket   
 
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4db34973a7244bdbb1ddaef5bd17a869"

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def get_ip_address():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unable to fetch IP"

def processcommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c:
        webbrowser.open("https://instagram.com")
    elif "open whatsapp" in c:
        webbrowser.open("https://web.whatsapp.com")
    elif "open chatgpt" in c or "open chat gpt" in c:
        webbrowser.open("https://chat.openai.com")
    elif "open gmail" in c:
        webbrowser.open("https://mail.google.com")
    elif "open maps" in c:
        webbrowser.open("https://www.google.com/maps")
    elif "open flipkart" in c:
        webbrowser.open("https://flipkart.com")
    elif "open tinder" in c:
        webbrowser.open("https://tinder.com")
    elif "open snapchat" in c:
        webbrowser.open("https://snapchat.com")
    elif "open deepseek" in c or "open deep seek" in c:
        webbrowser.open("https://chat.deepseek.com")
    elif c.startswith("play"):
        song = c.replace("play", "", 1).strip()
        possible_match = difflib.get_close_matches(song, musiclibrary.music.keys(),n = 1, cutoff = 0.6)
        if possible_match:
            link = musiclibrary.music[possible_match[0]]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")
    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                for article in articles[:5]:
                    speak(article["title"])
            else:
                speak("Sorry, I couldn't fetch the news.")
        except:
            speak("News API failed to connect.")
    elif "search" in c:
        query = c.replace("search", "").strip()
        if query:
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please say something to search.")
    elif "youtube" in c:
        query = c.replace("youtube", "").strip()
        if query:
            speak(f"Searching YouTube for {query}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    elif "time" in c:
        now = datetime.datetime.now()
        speak("Current time is " + now.strftime("%I:%M %p"))
    elif "date" in c:
        today = datetime.date.today()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}")
    elif "joke" in c:
        speak("Why don’t scientists trust atoms? Because they make up everything!")
    elif "ip address" in c:
        ip = get_ip_address()
        speak(f"Your IP address is {ip}")
    else:
        speak("Searching for an answer on Google...")
        webbrowser.open(f"https://www.google.com/search?q={c}")

# ========== VOICE ACTIVATED MAIN LOOP ==========

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("Listening for wake word...")

        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout = 5, phrase_time_limit = 5)
            wake = recognizer.recognize_google(audio)

            if wake.lower() == "jarvis":
                speak("Yes, I'm here! Listening for your command...")

                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout = 10)
                command = recognizer.recognize_google(audio)

                print("Command recognized:", command)
                processcommand(command)

        except Exception as e:
            print("Error:", e) 