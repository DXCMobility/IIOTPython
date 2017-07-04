import sys
import time
import Adafruit_DHT
import signal
from qhue import Bridge
import RPi.GPIO as GPIO
import signal
import sys
from select import select
import requests
import urllib2
import json
import requests

#function serviceCall
def service_call():
    response = urllib2.urlopen('https://dxciot.firebaseio.com/industry_switch.json')
    data = json.load(response)
    assembly_line = data['industry'][0]['assembly_line']['status']
    
    if assembly_line == True:
        assembly_line_status = True    
        start_assembly_line();
    else:
        assembly_line_status = False
        stop_assembly_line();

    generic_fan = data['industry'][0]['generic_fan']['status']
    print(generic_fan)

    if generic_fan == True:
        generic_fan_status = True
        start_generic_cooling_system();
    else:
        generic_fan_status = False
        stop_generic_cooling_system();

      

    load_object = load_check(generic_fan_status, assembly_line_status);

   # industry_object = {"industry":[{"assembly_cooling_fan":{"status":true,"value":22},"assembly_line":{"status":false,"value":22},"f1_bulbs":[{"status":true,"value":22},{"status":true,"value":12}],"generic_fan":{"status":true,"value":22},"humidity":{"status":true,"value":22},"power_consumption":"150","temp":{"status":true,"value":23}},{"f2_bulbs":[{"status":true,"value":22},{"status":true,"value":12}],"power_consumption":"100","sound":{"status":true,"value":23}},{"windmill":{"generated_power":434,"status":true}}]}

   # resp = requests.patch('https://dxciot.firebaseio.com/industry/industry/0.json')

   # resp = requests.patch('https://dxciot.firebaseio.com/industry/industry/0.json'',
                          #  json=industry_object,
                          #  headers={'Content-Type':'application/json'})
    #temp_object = {"assembly_line":{"status":assembly_line_status,"value":22},"generic_fan":{"status":generic_fan_status,"value":22}}
    #print(load_object)
    
    
           
#function to start motor
def start_assembly_line():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setup(27,GPIO.OUT)
    print "Assembly Line Started\n\n"
    GPIO.output(12,1)
    GPIO.output(25,0)
    GPIO.output(22,1)
    GPIO.output(27,0)
    time.sleep(2)
    
    
#function to stop motor
def stop_assembly_line():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    GPIO.setup(22,GPIO.OUT)
    GPIO.setup(27,GPIO.OUT)
    print "Alert : Assembly Line Stopped !\n\n"
    GPIO.output(12,0)
    GPIO.output(25,0)
    GPIO.output(22,0)
    GPIO.output(27,0)
    time.sleep(2)
    
    
#function to Generic Cooling System
def start_generic_cooling_system():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    print "Generic Cooling System Working Fine \n\n"
    GPIO.output(24,1)
    GPIO.output(23,0)
    time.sleep(2)

#function to Generic Cooling System
def stop_generic_cooling_system():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    print "Alert : Generic Cooling System Stopped !\n\n"
    GPIO.output(24,0)
    GPIO.output(23,0)
    time.sleep(2)  

#function to Assembly Cooling Fan
def start_assembly_cooling_fan():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    print "Alert : Assemble Cooling System Started ! \n\n"
    GPIO.output(26,1)
    GPIO.output(19,0)
    time.sleep(2)
    start_red_load();
    stop_green_load();
    time.sleep(2)

#function to Assembly Cooling Fan
def stop_assembly_cooling_fan():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    print "Alert : Assemble Cooling System Stopped ! \n\n"
    GPIO.output(26,0)
    GPIO.output(19,0)
    time.sleep(2)
    
   	
#function to test touch sensor
def load_check(generic_fan_status,assembly_line_status):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.IN)
    print "Touch Sensor Initialization \n\n"
    if GPIO.input(17) == GPIO.LOW:
       GPIO.setup(05,GPIO.OUT) 
       print "No Need For Cooling \n\n"
       assembly_cooling_fan_status = False
       f1_bulb_g_status = True
       f1_bulb_r_status = False
       stop_assembly_cooling_fan();
       start_green_load();
       stop_red_load();
       time.sleep(2)
    else:
        assembly_cooling_fan_status = True
        f1_bulb_g_status = False
        f1_bulb_r_status = True
        print "Alert : Cooling Required !\n\n"
        start_push_noti();
        start_assembly_cooling_fan();
        time.sleep(2)

    load_check_object = {"industry":[{"assembly_cooling_fan":{"status": assembly_cooling_fan_status,"value":130},"generic_fan":{"status":generic_fan_status,"value":22},"assembly_line":{"status":assembly_line_status,"value":22},"f1_bulbs":[{"status":f1_bulb_g_status,"value":22},{"status":f1_bulb_r_status,"value":12}],"humidity":{"status":True,"value":50},"power_consumption":"150","temp":{"status":True,"value":23}}]}
    print (load_check_object)
    resp = requests.patch('https://dxciot.firebaseio.com/industry.json')

    resp = requests.patch('https://dxciot.firebaseio.com/industry.json',
                            json=load_check_object,
                            headers={'Content-Type':'application/json'})

    #url = "https://indushpe.azure-devices.net/devices/rasp_industry_1/messages/events"

    #querystring = {"api-version":"2016-02-03"}

    #payload = load_check_object

    #headers = {'content-type': "application/json",'authorization': "SharedAccessSignature sr=indushpe.azure-devices.net&sig=m6OChGCR1n7%2FP%2FWWC%2FOufJOEBwcWY4rzzmFE8GXhF28%3D&skn=iothubowner",'cache-control': "no-cache",'postman-token': "ca3514c3-4af1-1609-df8c-21b9084c8a62"}

    #response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    #print(response.text)

    return load_check_object

#function pushNotification
def start_push_noti():
    url1 = "https://fcm.googleapis.com/fcm/send"

    #payload1 = "{ \"data\": {\r\n\"title\": \"Warning : Cooling System Enabled\"\r\n}, \"to\": \"eCzBTH1Yt-Q:APA91bH1R40fA2wqPuwok3oW6GSSCiyg6XUkUF4-v4PZHrdr-bmNfuS0DwTmYVPQv7f94xwLTyrh697u-jPai6bx7AgO-7JgiYB2zvqdZnvi7kTvCdIWSXatMcSnmeMXyjQ7N6XJCqS5\" }"
    payload1 = "{ \"data\": {\r\n\"title\": \"Warning : Cooling System Enabled\"\r\n}, \"to\": \"f3RxCAnJyFY:APA91bHcd2g8Gpvjt12pWQc9StfLIUJO0iEACWK-EkIaDPeNa7G5YsUr94bCKu6dBoHG1IshqhIj890lv6crhOlPCue7i8yZxJl0jA5Aqxf2GwVtlt7y-4tFyNE7fkrALKMCnfGxVe-Z\" }"
    headers1 = {
    'content-type': "application/json",
    'authorization': "key=AAAAiYBhpzY:APA91bEaEbaBXBrS1kr78wzFzWX4_GEMtDCEpO9U8SsAVtKXxgwvPcr9Ebd7f_Fsr9LqWo5nGorti6J64ztvqBIhwGZ_wN9wR0AKWdjv0RRx2iDXy7IOdjlRg-NSSaOtp1jiWuDD8Gyi"
    }

    response = requests.request("POST", url1, data=payload1, headers=headers1)

    print(response.text)
    
        
#function to  Green led
def start_green_load():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	print "Loads Status : Good \n\n"
	GPIO.output(21,GPIO.HIGH)
	time.sleep(2)
	
#function to Red led
def start_red_load():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(20,GPIO.OUT)
	print "Warning !! - Load Level Is High \n\n"
	GPIO.output(20,GPIO.HIGH)
	time.sleep(2)
	
#function to  Stop Green led
def stop_green_load():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	GPIO.output(21,GPIO.LOW)
	time.sleep(2)
	
#function to Red led
def stop_red_load():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(20,GPIO.OUT)
	GPIO.output(20,GPIO.LOW)
	time.sleep(2)
	

#First Time initialization

print "Initializing The Sensors....\n"
time.sleep(3)
print "Initialization Success\n\n"
time.sleep(0.5)

#Initiating User Feeds

while(1):
        service_call();
        
        
     

		
	

