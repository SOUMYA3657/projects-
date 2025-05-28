import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import pyjokes
import random
import subprocess
import time

class VoiceAssistant:
    def __init__(self):
        self.engine = self.init_tts()
        self.recognizer = sr.Recognizer()
        self.running = True
        self.open_apps = {}  

    def init_tts(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        try:
            for voice in voices:
                if 'david' in voice.id.lower() or 'zira' in voice.id.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                else:
                    engine.setProperty('voice', voices[0].id)
        except Exception:
            if len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 165)
        engine.setProperty('volume', 1.0)
        return engine
    
    def speak(self, text):
        """Speak text without printing it to console"""
        try:
            if len(text) > 50:
                parts = text.split('. ')
                for part in parts:
                    if part.strip():
                        self.engine.say(part.strip())
                        self.engine.runAndWait()
                        time.sleep(0.15)
            else:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception:
            pass

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                return self.recognizer.recognize_google(audio).lower()
            except:
                return ""

    def greet(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            self.speak("Good morning! How can I assist you?")
        elif 12 <= hour < 18:
            self.speak("Good afternoon! How can I help?")
        else:
            self.speak("Good evening! What can I do for you?")

    
    def handle_name_query(self):
        response = ("You can call me Voice Assistant, or whatever you prefer. "
                   "Just please don't call me by the names of other AI assistants.")
        self.speak(response)

    def handle_mood_query(self):
        response = ("Thank you for asking, but I'm a digital component "
                   "so I don't have feelings. However, I'm pleased to have "
                   "a friendship with a human like you.")
        self.speak(response)

    def handle_compliment_response(self):
        responses = ["Thank you!", "My pleasure!", "You're welcome!", "Glad to help!"]
        self.speak(random.choice(responses))

    def self_introduction(self):
        intro = ("I am an AI voice assistant created by you. My current capabilities include: "
                "telling time and date, searching Wikipedia, opening websites and applications, "
                "and telling jokes! I am keep improving my skills. ")
        self.speak(intro)

    
    def open_application(self, app_name):
        """Open various applications based on command"""
        app_commands = {
            'notepad': ['notepad.exe'],
            'paint': ['mspaint.exe'],
            'word': ['winword.exe'],
            'excel': ['excel.exe']
        }
        
        if app_name in app_commands:
            try:
                subprocess.Popen(app_commands[app_name])
                self.open_apps[app_name] = True
                self.speak(f"Opening {app_name}")
            except Exception:
                self.speak(f"Sorry, I couldn't open {app_name}")
        else:
            self.speak(f"I don't know how to open {app_name}")

    
    def process_command(self, command):
        if not command:
            return False

        if any(phrase in command for phrase in ["ok great", "great"]):
            self.handle_compliment_response()
            return False
            
        if "tell me about yourself" in command:
            self.self_introduction()
            return False

        if any(phrase in command for phrase in ["what is your name", "what should i call you"]):
            self.handle_name_query()
            return False

        if "how are you my friend" in command:
            self.handle_mood_query()
            return False

        if 'open' in command:
            if 'notepad' in command:
                self.open_application('notepad')
            elif 'paint' in command:
                self.open_application('paint')
            elif 'word' in command:
                self.open_application('word')
            elif 'excel' in command:
                self.open_application('excel')
            elif 'youtube' in command:
                self.open_website("youtube.com")
            elif 'google' in command:
                self.open_website("google.com")
            else:
                website = command.replace('open', '').strip()
                if website:
                    self.open_website(website)
                else:
                    self.speak("What would you like me to open?")
            return False

        if 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        elif 'wikipedia' in command:
            self.search_wikipedia(command.replace('wikipedia', ''))
        elif 'joke' in command:
            self.tell_joke()
        elif any(word in command for word in ['stop', 'exit', 'sleep']):
            self.speak("Goodbye! It was nice interacting with you.")
            return True
        else:
            self.speak("I didn't quite catch that. Could you please repeat?")
        return False

    
    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def get_date(self):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {current_date}")

    def search_wikipedia(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(result)
        except Exception:
            self.speak("Sorry, I couldn't find that information.")

    def open_website(self, url):
        try:
            url = url.strip()
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if '.' not in url:
                url += '.com'
                
            webbrowser.open(url)
            self.speak(f"Opening {url.split('//')[-1].split('/')[0]}")
        except Exception:
            self.speak("Sorry, I couldn't open that website.")

    def tell_joke(self):
        jokes = pyjokes.get_jokes(language='en', category='all')
        if not jokes:
            self.speak("I couldn't find any jokes to tell.")
            return
        self.speak(random.choice(jokes))


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.greet()
    
    while assistant.running:
        command = assistant.listen()
        if command:
            if assistant.process_command(command):
                assistant.running = False