import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import webbrowser
import os
import smtplib
import socket
import subprocess

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
running = True

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'tony' in command:
                command = command.replace('tony', '')
                print(f"Command: {command}")
    except:
        return ""
    return command

def send_email(to, subject, message):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to, email)
        server.quit()
        talk("Email sent successfully.")
    except Exception as e:
        talk("Failed to send the email.")
        print(e)

def wifi_radar():
    talk("Scanning for nearby Wi-Fi networks. Please wait.")
    try:
        result = subprocess.check_output("netsh wlan show networks", shell=True).decode('utf-8')
        networks = [line.strip() for line in result.split('\n') if "SSID" in line]
        for net in networks:
            talk(net)
    except:
        talk("Failed to scan Wi-Fi networks.")

def device_radar():
    talk("Scanning local network for active devices.")
    ip_base = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + '.'
    for i in range(1, 5):  
        ip = ip_base + str(i)
        result = os.system(f"ping -n 1 {ip} >nul")
        if result == 0:
            talk(f"Device found at {ip}")

def run_tony():
    global running
    command = take_command()
    print(f"You said: {command}")

    if 'play' in command:
        song = command.replace('play', '')
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'date' in command:
        date = datetime.datetime.now().strftime('%A, %B %d')
        talk(f"Today is {date}")

    elif 'open youtube' in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open notepad' in command:
        talk("Opening Notepad")
        os.system("notepad.exe")

    elif 'send email' in command:
        try:
            talk("Who is the recipient?")
            to = input("Enter recipient email: ")
            talk("What is the subject?")
            subject = take_command()
            talk("What is the message?")
            message = take_command()
            send_email(to, subject, message)
        except:
            talk("Sorry, I couldn't send the email.")

    elif 'shutdown system' in command:
        talk("Shutting down the system")
        os.system('shutdown /s /t 1')

    elif 'restart system' in command:
        talk("Restarting the system")
        os.system('shutdown /r /t 1')

    elif 'logout' in command:
        talk("Logging out")
        os.system('shutdown -l')

    elif 'wifi radar' in command:
        wifi_radar()

    elif 'device radar' in command:
        device_radar()

    elif 'rest' in command or 'exit' in command:
        talk("Stopping the assistant. Goodbye!")
        running = False

    else:
        talk("Please say that again.")

while running:
    run_tony()
