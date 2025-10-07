import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import time
import pyautogui
import pygetwindow as gw

# Api key
client = OpenAI(api_key="")

# Voice Settings
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def waitforinput():
    command = listen()
    if "Johnny" in command:
        assistant()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source, timeout=10)

    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

    
def ask_openai(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": question}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def assistant():
    speak("Hello! How can I assist you today?")
    while True:
        try:
            command = listen()
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            elif "close firefox" in command or "close fire" in command:
                try:
                    import pygetwindow as gw
                    import pyautogui
                    import time

                    print("Closing Firefox...")
                    speak("Closing Firefox")

                    firefox_windows = gw.getWindowsWithTitle("Mozilla Firefox")
                    if firefox_windows:
                        window = firefox_windows[0]
                        window.activate()
                        time.sleep(0.4)
                        pyautogui.hotkey("alt", "f4")
                    else:
                        print("Firefox window not found.")
                        speak("I couldn't find Firefox running.")
                except Exception as e:
                    print(f"Error closing Firefox: {e}")
                    speak("Sorry, I couldn't close Firefox.")
            elif "firefox" in command or "fire" in command:
                try:
                    print(f"Opening Firefox...")
                    speak("Opening Firefox")
                    os.system("start firefox")
                except Exception as e:
                    print(f"Error opening Firefox: {e}")
                    speak("Sorry, I couldn't open Firefox")
            elif "sleep mode" in command or "sleep" in command:
                try:
                    print(f"Entering Sleep mode")
                    speak("Entering Sleep mode right now")
                except Exception as e:
                    print(f"Error in Sleep mode Activation")
                    speak("Error in Sleep Mode")
#            elif "esesha" in command or "ssh" in command:
#                try:
#                    print(f"Openning ssh connection with a 192.168.55.112")
#                    speak("Openning ssh")
#                    os.system("ssh root@192.168.55.112")
#                except Exception as e:
#                    print(f"Error opening ssh")
#                    speak("Sorry I couldn't open ssh")
#            elif "close terminal" in command:
 #               try:
 #               print(f"Closing terminal")
 #               speak("Closing termnal now")
 #               os.system("taskkill /im cmd.exe")
 #               except Exception as e:
 #                   print(f"I couldn't close the terminal")
 #                   speak("Terminal")
            # Komendy wymagające OpenAI
            elif "cybertron" in command: # To jest cyber Johnny ale speech recognition is dumb af
                speak("What do you want, V?")
                time.sleep(1)
                while True:
                    question = listen()
                    if "exit johnny" in question or "go back" in question:
                        speak("Later, V.")
                        break
                    elif question:
                        try:
                            response = ask_openai(question)
                            if response:
                                print(f"Johnny: {response}")
                                speak(response)
                                assistant()
                            else:
                                print("DEBUG: OpenAI zwróciło pustą odpowiedź")
                        except Exception as e:
                            print("DEBUG: błąd OpenAI:", e)
                            speak("Can't hear you, V.")

        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as e:
            print("DEBUG: błąd w listen():", e)


if __name__ == "__main__":
    waitforinput()
