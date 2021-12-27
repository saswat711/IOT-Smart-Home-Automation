
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import ano_det
import time
from threading import Thread

class CountdownTask:
      
    def __init__(self):
     self._running = True
      
def terminate(self):
    self._running = False
      
def run(self, n):
    while self._running and n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty("rate", 174)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("good morning sir")
    elif hour <= 0 and hour >=12:
        speak("good afternoon sir")
    else:
        speak("good evening sir")
    
    speak("I am Friday your personal virtual assistant system at your service")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5 
        
        audio = r.listen(source)
    try: 
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-us")
        print(f"user said: {query} \n ")
    except Exception as e:
        print(e) # it print the error

        print("Say that again please...")
        return"None"
    return query
 
def sendmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('saswatmund711@gmail.com', 'Salman44!!!!')
    server.sendmail('saswatmund711@gmail.com',to,content)
    server.close()
    
def forQuery():
      query = takecommand().lower()
        
      if "Wikipedia" in query:
            speak("Searching wikipedia...")
            query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 1 )
            speak("According to wikipedia")
            print(results)
            speak(results)
            return 0
      
      elif "open YouTube" in query:
            webbrowser.open("youtube.com")
            return 0
      
      elif "open stackoverflow" in query:
            webbrowser.open("stackoverflow")
            return 0
      
      elif "open Google" in query:
            webbrowser.open("google.com")
            return 0
      
      elif "play music" in query:
            music_dir = "E:\\movies\\Boruto_ Naruto Next Generations OP_Opening 9 Full『Gamushara』by CHiCO with HoneyWorks(MP3_320K).mp3"
            songs = os.listdir(music_dir)
            #print(songs)
            a = random.randint(1,147)
            os.startfile(os.path.join(music_dir, songs[a]))
            return 0
      
      elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")
            return 0
      
      elif "email to me" in query:
            try:
                speak('what do you want to speak')
                content = takecommand()
                to = "saswatmund711@gmail.com"
                sendmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("sorry sir i am not able to send this email...")
            return 0
      
      elif "turn off" in query or "off the lights" in query or "turn off the lights" in query:
            print("Turning off the lights")
            speak("Turning off the lights")
            ano_det.toSwitchLight(False)
            return 0
      
      elif "turn on" in query or "on the lights" in query or "turn on the lights" in query:
            print("Turning on the lights")
            speak("Turning on the lights")
            ano_det.toSwitchLight(True)
            return 0
      
      elif "check light" in query or "status of my lights" in query:
            print("Checking if light is on or off") 
            speak("Checking if light is on or off")
            status =  ano_det.toCheckLight()
            if status:
               speak ("It seems like the light is on")
               print ("It seems like the light is on")

            else:
               speak("It seems like the light is off")
               print("It seems like the light is off")
            return 0
      
      elif "run security" in query or "security" in query:
           """ To run security if light is on or not """
           print("Running the security protocol")
           speak("Running the security protocol")
           thread1.start()
           return 0
      
      elif "thank you bye" in query:
            speak("Your welcome Sir")
            return 1
         
      elif "exit" in query:
            speak("Shutting Down")
            exit()
            return 2

def atStart(init):
 while True:
   text = takecommand().lower()
   if(text.count(wake[0]) or text.count(wake[1]) or text.count(wake[2]) or text.count(wake[3]))>0:
      if init==0:
         wishMe()
         init=1
         return init      

thread1 = Thread(target=ano_det.runSecAlert,daemon=True)
wake = ["you there","hey friday","hey friday are you there","hello miss friday"]   
print("Say you there to Wake up the assistant")
initial = atStart(0)

while True: 
      if initial ==0 :    
         initial = atStart(0)
         
      else:    
         x = forQuery()   
         if(x==1):
            initial = 0
            
         elif(x==2):
            break
      