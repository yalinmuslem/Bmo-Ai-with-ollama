import pyttsx3
engine = pyttsx3.init('sapi5')
engine.say("Hello, can my voice be heard?")
engine.runAndWait()