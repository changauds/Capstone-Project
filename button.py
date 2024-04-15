import RPi.GPIO as GPIO
import time
from signal import pause
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#tap1 = Button(2) #Switch that detects tap handle position

def setTimer(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t-=1
    print('Good job brushing!')
t = 120

def displayData():
    # read from data.json
    tooth_j_file = open('data.json', "r")
    data = json.load(tooth_j_file.read())
    for i in data['emp_details']:
        print(i)
    f.close()
try:
    while True:
        if (GPIO.input(23)):
            setTimer(t)
            displayData()
except KeyboardInterrupt:
    pass
    

GPIO.cleanup()

