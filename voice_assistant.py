import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyjokes
import os

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak Function
def speak(text):
    st.session_state['log'].append(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen from mic
def listen_command():
    with sr.Microphone() as source:
        st.session_state['log'].append("🎙 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            st.session_state['log'].append("🔍 Recognizing...")
            command = recognizer.recognize_google(audio)
            st.session_state['log'].append(f"✅ You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

# Handle commands
def handle_command(command):
    if "hello" in command:
        speak("Hey there! How can I help?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")

    elif "search" in command:
        speak("What do you want to search?")
        query = listen_command()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the results for {query}")

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "note" in command or "write" in command:
        speak("What should I write?")
        note = listen_command()
        if note:
            with open("quick_note.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            speak("Note saved.")

    elif "open" in command:
        sites = ["facebook", "instagram", "twitter", "github"]
        for word in sites:
            if word in command:
                url = f"https://www.{word}.com"
                webbrowser.open(url)
                speak(f"Opening {word}")
                return

    elif "what can you do" in command:
        speak("I can tell the time, date, search the web, open YouTube, tell jokes, and take notes. Just say a command!")

    elif "bye" in command or "exit" in command:
        speak("Goodbye, buddy!")

    else:
        speak("I didn't understand that. Try saying hello, time, date, search, YouTube, or bye.")

# Streamlit UI
st.set_page_config(page_title="Voice Assistant", layout="centered")

if 'log' not in st.session_state:
    st.session_state['log'] = []

st.title("🧠 Voice Assistant")
st.markdown("Press the button and speak your command...")

if st.button("🎤 Start Listening"):
    command = listen_command()
    if command:
        handle_command(command)

# Display output log
st.subheader("📝 Assistant Log")
for line in st.session_state['log']:
    st.write(line)
