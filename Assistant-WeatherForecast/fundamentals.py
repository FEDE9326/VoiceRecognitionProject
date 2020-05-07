# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:09:37 2020

@author: fede9326
"""

import pygame
import speech_recognition as sr_audio
import pyttsx3
import spacy
from spacy.matcher import Matcher
import requests

# openweathermap API_Key
weather_api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
# base_url variable to store url 
openweathermap_url = "http://api.openweathermap.org/data/2.5/weather?"  

def read_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
def play_sound(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
def weather_forecast(city):
    print("Fecthing the weather in " + city)   
    
    complete_url = openweathermap_url + "appid=" + weather_api_key + "&q=" + city
    
    # retrieving data through get API
    response = requests.get(complete_url) 
       
    # convert response into json 
    data = response.json() 
    
    # Checking if the city was found
    if data["cod"] != "404": 
          
        # storing value of key "temp" and converting int celsius
        current_temperature = round(data["main"]["temp"] - 273.15)
          
        # storing the weather description 
        weather_description = data["weather"][0]["description"] 
        
        # returning the complete string
        return "The weather in " + city + "is: " + weather_description + " with a temperature of " + str(current_temperature) + " grad celsius."
          
    else: 
        return "City Not Found"
    
def one_shot_weather_forecast():
    
    # Loading spacy dictionary
    nlp = spacy.load('en')
    
    # Bot question
    read_text("Hi, would you like to know the weather forecast?")
    
    # Recording answer after the beep
    mic = sr_audio.Microphone()
    r = sr_audio.Recognizer()
    with mic as source:
        play_sound("beep.mp3")
        audio = r.listen(source, phrase_time_limit=10)
        print("Finish Recording. Performing Speech Recognition")
    
    # Calling Google Cloud Service or sphinx
    text = ""
    try: 
        text = r.recognize_google_cloud(audio)
        # text = r.recognize_sphinx(audio)
    except:
        print("No reponse from Cloud Service")
    print("The recognized text is: " + text)
    
    # Text analysis with Spacy. Creating Spacy Document
    doc = nlp(text)
    
    # Creating a matcher for the yes/no answer
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "yes"}]
    matcher.add("Positive", None, pattern)
    
    # Extracting the city in case of Positive response. Cities are grouped into label 
    # "GPE" or sometimes "ORG".
    city = ""
    if len(matcher(doc)) > 0:
        for ent in doc.ents:
            if ent.label_ == "GPE" or "ORG":
                city = ent.text
                break
            
    if city != "":
        print("The selected city is: " + city)
        
        # retrieving weather info through openweathermap API
        weather_forecast_string = weather_forecast(city)
        
        # reading information
        read_text(weather_forecast_string)
        
    else:
        print("The service was not able to recognize the city")
        
 
if __name__ == "__main__":
    one_shot_weather_forecast()



