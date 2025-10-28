# import speech_recognition as sr
# import pyttsx3
# import ollama
# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import threading

# # Global flag to control the listening thread
# listening_active = False
# def speak(text):
#     """Conv
#     rt text to speech and speak it out loud."""
#     engine = pyttsx3.init()
#     engine.setProperty("rate", 170)
#     engine.say(text)
#     engine.runAndWait()

# def recognize_speech():
#     """Listen to user speech and convert it to text."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         status_label.config(text="Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
#             text = recognizer.recognize_google(audio).lower()
#             status_label.config(text="Processing...")
#             return text
#         except sr.UnknownValueError:
#             status_label.config(text="Could not understand audio.")
#             return None
#         except sr.RequestError:
#             status_label.config(text="Could not request results, check internet.")
#             return None
#         except sr.WaitTimeoutError:
#             status_label.config(text="Listening timed out.")
#             return None

# def get_ai_response(user_input):
#     """Get AI response using Ollama."""
#     if "your name" in user_input:
#         return "My name is Verna."
#     elif "who developed you" in user_input:
#         return "I was developed by Robo Miracle."
#     else:
#         try:
#             response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
#             return response['message']['content']  # Removed truncation
#         except Exception as e:
#             print(f"Error in AI response: {e}")
#             return "I am having trouble responding."

# def start_listening():
#     """Start listening and respond."""
#     global listening_active
#     listening_active = True

#     def listen_and_respond():
#         while listening_active:
#             user_input = recognize_speech()
#             if user_input:
#                 chat_log.insert(tk.END, f"You: {user_input}\n", "user")
#                 if "stop" in user_input:
#                     stop_conversation()
#                     return
#                 ai_response = get_ai_response(user_input)
#                 chat_log.insert(tk.END, f"Verna: {ai_response}\n", "verna")
#                 chat_log.yview(tk.END)
#                 speak(ai_response)
#                 status_label.config(text="Click the button to speak")
    
#     # Run the listening and responding function in a separate thread
#     threading.Thread(target=listen_and_respond, daemon=True).start()

# def stop_conversation():
#     """Stop the conversation."""
#     global listening_active
#     listening_active = False
#     status_label.config(text="Conversation stopped.")
#     chat_log.insert(tk.END, f"Verna: Goodbye! Conversation stopped.\n", "verna")
#     chat_log.yview(tk.END)
#     speak("Goodbye! Conversation stopped.")

# # UI Setup
# root = tk.Tk()
# root.title("Verna - Voice Assistant")
# root.geometry("400x500")
# root.configure(bg="#f0f0f0")

# title_label = tk.Label(root, text="Verna - Voice Assistant", font=("Arial", 14, "bold"), bg="#f0f0f0")
# title_label.pack(pady=10)

# chat_log = scrolledtext.ScrolledText(root, width=50, height=15, font=("Arial", 10))
# chat_log.pack(padx=10, pady=10)
# chat_log.tag_configure("user", foreground="blue")
# chat_log.tag_configure("verna", foreground="green")

# status_label = tk.Label(root, text="Click the button to speak", font=("Arial", 12), bg="#f0f0f0")
# status_label.pack(pady=10)

# speak_button = tk.Button(root, text="Speak", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", padx=20, pady=10, command=start_listening)
# speak_button.pack(pady=10)

# stop_button = tk.Button(root, text="Stop", font=("Arial", 12, "bold"), bg="#DC3545", fg="white", padx=20, pady=10, command=stop_conversation)
# stop_button.pack(pady=10)

# exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#DC3545", fg="white", command=root.quit)
# exit_button.pack(pady=10)

# # Initial greeting
# initial_message = "Hi, I am Verna.welcome to tamil nadu,Enjoy your journey,How can I help you?"
# chat_log.insert(tk.END, f"Verna: {initial_message}\n", "verna")
# speak(initial_message)

# root.mainloop()

import speech_recognition as sr
import pyttsx3
import ollama
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Global flag to control the listening thread
listening_active = False

def speak(text):
    """Convert text to speech and speak it out loud."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Select female voice
    engine.setProperty("rate", 160)  # Slightly reduced speed for clarity
    engine.setProperty("volume", 1.0)  # Ensure max volume
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Listen to user speech and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)  # Increased duration for better accuracy
        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()
            status_label.config(text="Processing...")
            return text
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio.")
            return None
        except sr.RequestError:
            status_label.config(text="Could not request results, check internet.")
            return None
        except sr.WaitTimeoutError:
            status_label.config(text="Listening timed out.")
            return None

def get_ai_response(user_input):
    """Get AI response using Ollama."""
    if "your name" in user_input:
        return "My name is MJ."
    elif "who developed you" in user_input:
        return "I was developed by iRobotics."
    else:
        try:
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])
            return response.get('message', {}).get('content', "I am having trouble responding.")
        except Exception as e:
            print(f"Error in AI response: {e}")
            return "I am having trouble responding."

def start_listening():
    """Start listening and respond."""
    global listening_active
    listening_active = True

    def listen_and_respond():
        while listening_active:
            user_input = recognize_speech()
            if user_input:
                chat_log.insert(tk.END, f"You: {user_input}\n", "user")
                if "stop" in user_input:
                    stop_conversation()
                    return
                ai_response = get_ai_response(user_input)
                chat_log.insert(tk.END, f"MJ: {ai_response}\n", "mj")
                chat_log.yview(tk.END)
                speak(ai_response)
                status_label.config(text="Click the button to speak")
    
    threading.Thread(target=listen_and_respond, daemon=True).start()

def stop_conversation():
    """Stop the conversation."""
    global listening_active
    listening_active = False
    status_label.config(text="Conversation stopped.")
    chat_log.insert(tk.END, f"MJ: Goodbye! Conversation stopped.\n", "mj")
    chat_log.yview(tk.END)
    speak("Goodbye! Conversation stopped.")

# UI Setup
root = tk.Tk()
root.title("MJ - Voice Assistant")
root.geometry("400x500")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="MJ - Voice Assistant", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

chat_log = scrolledtext.ScrolledText(root, width=50, height=15, font=("Arial", 10))
chat_log.pack(padx=10, pady=10)
chat_log.tag_configure("user", foreground="blue")
chat_log.tag_configure("mj", foreground="green")

status_label = tk.Label(root, text="Click the button to speak", font=("Arial", 12), bg="#f0f0f0")
status_label.pack(pady=10)

speak_button = tk.Button(root, text="Speak", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", padx=20, pady=10, command=start_listening)
speak_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", font=("Arial", 12, "bold"), bg="#DC3545", fg="white", padx=20, pady=10, command=stop_conversation)
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Arial", 12), bg="#DC3545", fg="white", command=root.quit)
exit_button.pack(pady=10)

# Initial greeting
initial_message = "Hi, I am MJ.How can I help you?"
chat_log.insert(tk.END, f"MJ: {initial_message}\n", "mj")
speak(initial_message)

root.mainloop()