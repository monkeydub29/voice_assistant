#!/usr/bin/env python
# coding: utf-8

# In[1]:
import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import wolframalpha
import pywhatkit


# In[2]:


wolfram_api = '8LQY83-RTHG64QQGG'

def alex_listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        text = ''

        try:
            text = r.recognize_google(audio)
        except sr.RequestError as re:
            print(re)
        except sr.UnknownValueError as uve:
            print(uve)
        except sr.WaitTimeoutError as wte:
            print(wte)

    text = text.lower()
    return text

def alex_talk(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    file_path = os.path.join(os.getcwd(), "audio_data.mp3")
    tts.save(file_path)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def alex_translate_speak(text):
    if 'say in hindi' in text:
        phrase = text.replace("say in hindi", "").strip()
        alex_talk(phrase, lang='hi')

    elif 'say in tamil' in text:
        phrase = text.replace("say in tamil", "").strip()
        alex_talk(phrase, lang='ta')

    elif 'say in english' in text:
        phrase = text.replace("say in english", "").strip()
        alex_talk(phrase, lang='en')

    else:
        alex_talk("Please say something like 'say in Hindi I am happy'.")

def wolfram_query(text):
    client = wolframalpha.Client(wolfram_api)
    try:
        result = client.query(text)
        answer = next(result.results).text
        alex_talk(answer)
    except Exception as e:
        alex_talk("Sorry, I couldn't understand or compute that.")
        print(e)

def alex_play_youtube(text):
    try:
        query = text.replace("play", "").replace("on youtube", "").strip()
        alex_talk(f"Playing {query} on YouTube")
        pywhatkit.playonyt(query)
    except:
        alex_talk("I couldn't open YouTube right now.")

def alex_reply(text):
    if 'your name' in text:
        alex_talk('My name is Alex, your personal assistant.')

    elif 'why do you exist' in text:
        alex_talk("I was created to assist you 24/7 with no holidays!")

    elif 'when do you sleep' in text:
        alex_talk("I never sleep. I'm always here to help you.")

    elif 'are you stupid' in text:
        alex_talk("I'm learning every day. I try my best, always!")

    elif 'favourite movie' in text:
        alex_talk("My favorite movie is Titanic.")

    elif 'capital of' in text:
        wolfram_query(text)

    elif 'calculate' in text or 'solve' in text or 'math' in text:
        wolfram_query(text)

    elif 'what is' in text or 'who is' in text or 'how much' in text or 'distance' in text or 'convert' in text or 'time in' in text:
        wolfram_query(text)

    elif 'say in' in text:
        alex_translate_speak(text)

    elif 'play' in text and 'youtube' in text:
        alex_play_youtube(text)

    elif 'stop' in text or 'exit' in text:
        alex_talk('It was a pleasure helping you. Goodbye!')
        exit()

    else:
        alex_talk("I'm not sure I understood that. Can you repeat?")



# In[3]:


def execute_assistant():
    alex_talk('hi, I am here to support you. can you please tell me your name?')
    listen_name = alex_listen()
    print("User's name:", listen_name)
    alex_talk('Hi ' + listen_name + ' what can I do for you?')  # Corrected variable name
    
    while True:
        listen_alex = alex_listen()
        print("User input:", listen_alex)
        alex_reply(listen_alex)
        
        if 'stop' in listen_alex:
            break
        
        
execute_assistant()


# In[ ]:


client = wolframalpha.Client(wolfram_api)
result = client.query('what is the capital of russia?')
answer = next(result.results).text
print(answer)

