import conf,requests, json, time, math, statistics
from boltiot import Sms, Bolt
import CheckLight as cl



def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size]
    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1]+Zn
    Low_bound = history_data[frame_size-1]-Zn
    print(High_bound,Low_bound)
    return [High_bound,Low_bound]

def trigger_webhook(message):
    URL ="https://hook.integromat.com/i4p9o2g8mae4rdiv6lcn1372dq86wl6f" # REPLACE WITH CORRECT URL
    response = requests.request("GET", URL)
    print(response.text)

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
history_data=[]

pir_pin = 7
res1 = mybolt.serialBegin(9600)
ledPin = 4

def runSecAlert():

 """ To check light intensity if some one had turn on or not"""
 """ Also to check for intruder using PIR sensor"""
 while True:   
    #sending command to arduino to get serial data
    mybolt.serialWrite("GetPirData")
    
    Piresponse = mybolt.serialRead(7)
    data = json.loads(Piresponse)
    if data['success'] != 1:
        print("There was an error while retriving the pir data.")
        print("This is the pir error:"+data['value'])
        continue

    print ("This is the pir value "+data['value'])
    try:

        pirVal = data['value'].split(",")[0]
        print ("After Split pir "+pirVal)
        if pirVal == " 1":
            pirVal = True
        else:
            pirVal = False    
    except e:
        print("There was an error while parsing the pir response: ",e)
        continue

    print(pirVal," is the final pir val \n \n")
    if pirVal:
        response = trigger_webhook("Intruder detected")
    time.sleep(10)
    # FOR LDR
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    if data['success'] != 1:
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        continue

    print ("This is the value "+data['value'])
    sensor_value=0
    
    try:
        sensor_value = int(data['value'])
    except e:
        print("There was an error while parsing the response: ",e)
        continue

    bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
    
    if not bound:
        required_data_count=conf.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(int(data['value']))
        time.sleep(10)
        continue

    try:
        if sensor_value > bound[0] :
            print ("The light level increased suddenly. Sending an SMS.")
            response = trigger_webhook("Someone turned on the lights")
            print("This is the response ",response)
        elif sensor_value < bound[1]:
            print ("The light level decreased suddenly. Sending an SMS.")
            response = trigger_webhook("Someone turned off the lights")
            print("This is the response ",response)
        history_data.append(sensor_value);
    except Exception as e:
        print ("Error",e)
    
    time.sleep(10)  

def toCheckLight():
    """ to check if light is on or not """   
    if cl.Readlight():
        return True
    else:
        return False

def toSwitchLight(check):   
  if check:
    """ Turn on the light """
    cl.Writelight(True)
    mybolt.serialWrite("LED_ON")

  else:
    """ Turn off the light """ 
    cl.Writelight(False)
    mybolt.serialWrite("LED_OFF")