import sys
import time
import RPi.GPIO as GPIO
import signal
import sys
from select import select
import requests
import urllib2
import json
import math

def function_call():
    response = urllib2.urlopen('https://dxciot.firebaseio.com/industry.json')    
    data = json.load(response)
    assembly_cooling_fan = (data['industry'][0]['assembly_cooling_fan']['status'])
    print assembly_cooling_fan

    if assembly_cooling_fan == True:
            print "Service Started!!"
            url = "https://ussouthcentral.services.azureml.net/workspaces/0670f5082d194aa0ac093baefe5b3719/services/09e729684ca84050a3a9c4baecaf45ff/execute"
            querystring = {"api-version":"2.0","details":"true"}
            payload = "{\r\n  \"Inputs\": {\r\n    \"input1\": {\r\n      \"ColumnNames\": [\r\n        \"Relative Compactness\",\r\n        \"Surface Area\",\r\n        \"Wall Area\",\r\n        \"Roof Area\",\r\n        \"Overall Height\",\r\n        \"Orientation\",\r\n        \"Glazing Area\",\r\n        \"Glazing Area Distribution\",\r\n        \"Heating Load\",\r\n        \"Cooling Load\",\r\n        \"Duration\"\r\n      ],\r\n      \"Values\": [\r\n        [\r\n          \"0\",\r\n          \"637\",\r\n          \"0\",\r\n          \"0\",\r\n          \"7\",\r\n          \"3\",\r\n          \"0\",\r\n          \"0\",\r\n          \"29.9\",\r\n          \"0\",\r\n          \"0\"\r\n        ]\r\n      ]\r\n    }\r\n  }\r\n}\r\n"
            
            headers = {
                'content-type': "application/json",
                'authorization': "Bearer RXXCCNHa5uuXGzH97OAtRHxgtlT0xMBfXpFSh/WGdTAOb0HRJ5iLIclhNy1RP2yy65Q3WJHk61blgfP51vlkrg==",
                'cache-control': "no-cache",
                'postman-token': "ff447368-80e5-42e8-8bfd-132a1a8dd6be"
                } 
            response = requests.request("POST", url, data=payload, headers=headers, params=querystring) 
            azure_response = response.json()
            final_Response = (azure_response['Results']['output1']['value']['Values'][0][5])
            val = int(round(float(final_Response)))
            time.sleep(val);
            start_alarm();
            stop_alarm();
	    
            print val



   # else: 
        # stop_alarm();
         #stop_red_led();
         
            

    
#function to test sound sensor
def start_alarm():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18,GPIO.HIGH)
    print "BUZZER: ALARM !!"
    stop_green_led();
    start_fan();
    time.sleep(2)
    
    
#function to test sound sensor
def stop_alarm():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18,GPIO.LOW)
    print "System Working Fine"
    
    time.sleep(2)
    start_green_led();
    
def start_fan():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(12,GPIO.OUT)
    GPIO.output(12,GPIO.HIGH)
    time.sleep(2)
    

   
#function to test led
def start_green_led():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(26,GPIO.OUT)
	GPIO.output(26,GPIO.HIGH)
        status_fac2 = True 		
	

        factory2_check_object = {"status": status_fac2}
	print (factory2_check_object)
        resp = requests.patch('https://dxciot.firebaseio.com/industry_switch/industry/0/f1_bulbs/0.json')
        resp = requests.patch('https://dxciot.firebaseio.com/industry_switch/industry/0/f1_bulbs/0.json',json=factory2_check_object,headers={'Content-Type':'application/json'})


	time.sleep(2)
	
#function to test led
def stop_green_led():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(26,GPIO.OUT)
	GPIO.output(26,GPIO.LOW)
	time.sleep(2)

#function to test led
def start_red_led():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	GPIO.output(21,GPIO.HIGH)
	time.sleep(2)
	
#function to test led
def stop_red_led():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	GPIO.output(21,GPIO.LOW)
	time.sleep(2)	
	
def reset():
        stop_green_led()
        reset_status_fac2 = False
        reset_factory2_check_object = {"status": reset_status_fac2}
	print (reset_factory2_check_object)
        resp = requests.patch('https://dxciot.firebaseio.com/industry_switch/industry/0/f1_bulbs/0.json')
        resp = requests.patch('https://dxciot.firebaseio.com/industry_switch/industry/0/f1_bulbs/0.json',json=reset_factory2_check_object,headers={'Content-Type':'application/json'})
        
#First Time initialization

print "Initializing The Sensors....\n"
time.sleep(3)
print "Initialization Success\n\n"
time.sleep(0.5)
reset()


#Initiating User Feeds

while(1):
       
       function_call();
       
        
	
