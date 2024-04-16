import RPi.GPIO as GPIO
import time
from signal import pause
import os

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
    # Change this to the ABSOLUTE path of toothbrush.py on the rpi
    os.system("python toothbrush.py --show")


try:
    while True:
        if (GPIO.input(23)):
            setTimer(t)
            displayData()
except KeyboardInterrupt:
    pass
    

GPIO.cleanup()

