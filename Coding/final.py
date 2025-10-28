import speech_recognition as sr
import pyttsx3
import ollama
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from datetime import datetime

# Global flag to control the listening thread
listening_active = False

# Initialize engine globally
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

# Predefined responses
predefined_responses = {
    "your name": "My name is ML.",
    "who developed you": "I was developed by iRobotics.",
    "how are you": "I'm doing well, thank you!",
    "what is the time": f"The time is {datetime.now().strftime('%I:%M %p')}.",
}

def speak(text):
    """Convert text to speech and speak it out loud."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Recognize speech using the microphone."""
    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except OSError:
        status_label.config(text="Microphone not found.")
        return None

    status_label.config(text="Listening... Please speak now.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            status_label.config(text="Processing...")
            text = recognizer.recognize_google(audio).lower()
            return text
        except sr.WaitTimeoutError:
            status_label.config(text="Listening timed out.")
        except sr.UnknownValueError:
            status_label.config(text="Sorry, I could not understand.")
        except sr.RequestError as e:
            status_label.config(text="Speech recognition service error.")
            print(f"Speech recognition error: {e}")
        return None

def get_ai_response(user_input):
    """Get AI response using Ollama or predefined."""
    for key, value in predefined_responses.items():
        if key in user_input:
            return value
    try:
        response = ollama.chat(model="llama2", messages=[{"role": "user", "content": user_input}])
        return response.get('message', {}).get('content', "I am having trouble responding.")
    except Exception as e:
        print(f"Error in AI response: {e}")
        return "I am having trouble responding."

def start_listening():
    """Start listening and respond."""
    global listening_active
    if listening_active:
        return  # Prevent multiple threads
    listening_active = True
    speak_button.config(state=tk.DISABLED)

    def listen_and_respond():
        while listening_active:
            user_input = recognize_speech()
            if user_input:
                chat_log.insert(tk.END, f"You: {user_input}\n", "user")
                if "stop" in user_input:
                    stop_conversation()
                    return
                ai_response = get_ai_response(user_input)
                chat_log.insert(tk.END, f"ML: {ai_response}\n", "ml")
                chat_log.yview(tk.END)
                speak(ai_response)
                status_label.config(text="Click the button to speak")
        speak_button.config(state=tk.NORMAL)

    threading.Thread(target=listen_and_respond, daemon=True).start()

def stop_conversation():
    """Stop the conversation."""
    global listening_active
    listening_active = False
    status_label.config(text="Conversation stopped.")
    chat_log.insert(tk.END, f"ML: Goodbye! Conversation stopped.\n", "ml")
    chat_log.yview(tk.END)
    speak("Goodbye! Conversation stopped.")
    speak_button.config(state=tk.NORMAL)

def exit_app():
    """Clean exit."""
    stop_conversation()
    root.quit()

# UI Setup
root = tk.Tk()
root.title("ML - Voice Assistant")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="ML - Voice Assistant", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

chat_log = scrolledtext.ScrolledText(root, width=50, height=15, font=("Arial", 10))
chat_log.pack(padx=10, pady=10)
chat_log.tag_configure("user", foreground="blue")
chat_log.tag_configure("ml", foreground="green")
chat_log.tag_configure("ml", foreground="purple")

status_label = tk.Label(root, text="Click the button to speak", font=("Arial", 12), bg="#f0f0f0")
status_label.pack(pady=10)

speak_button = tk.Button(root, text="Speak", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", padx=20, pady=10, command=start_listening)
speak_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", font=("Arial", 12, "bold"), bg="#DC3545", fg="white", padx=20, pady=10, command=stop_conversation)
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#35DC91", fg="white", command=exit_app)
exit_button.pack(pady=10)

# Initial greeting with time
current_hour = datetime.now().hour
if current_hour < 12:
    greeting = "Good morning!"
elif current_hour < 18:
    greeting = "Good afternoon!"
else:
    greeting = "Good evening!"

initial_message = f"{greeting} I am ML. How can I help you?"
chat_log.insert(tk.END, f"ML: {initial_message}\n", "ml")
speak(initial_message)

root.mainloop()