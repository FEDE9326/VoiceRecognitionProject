This is an example on how to use the speec_recognition package. The application is intented to be a semplified vocal assistant which 
retrieves the weather in a city specified by the user with voice.

1) For reading a text *pyttsx3* is used
2) For collecting a record from the main microphone: Recognizer and Microphone Class from speech_recognition package
3) Google Cloud Service is used for Speech recognition through the *recognize_google_cloud* method of the Recognizer class (A subscription to Google Cloud Services is required).
4) For understanding the city inside a recognized text, *Spacy* is used. Spacy is a NLP Python library which allows to perform text analysis (https://spacy.io/).
5) Weather information are collected through the openweathermap APIs (https://openweathermap.org/api). Basic access to the APIs is free.


