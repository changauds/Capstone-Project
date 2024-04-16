import RPi.GPIO as GPIO
import time
from signal import pause
import json

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def setTimer(duration):
    stopwatch = 0
    while True:
        if duration >= 0:
            mins_timer, secs_timer = divmod(duration, 60)
            timer_display = '{:02d}:{:02d}'.format(mins_timer, secs_timer)

            mins_stopwatch, secs_stopwatch = divmod(stopwatch, 60)
            stopwatch_display = '{:02d}:{:02d}'.format(mins_stopwatch, secs_stopwatch)

            print("TIMER: ", timer_display, end="\r")
            print("STOPWATCH: ", stopwatch_display, end="\r")
            time.sleep(1)
            
            duration -= 1
            stopwatch += 1
        if (GPIO.input(23)):
            return stopwatch_display
            print("returned stopwatch_display!")
            break

    print('Good job brushing!')

def displayData():
    # read from data.json
    tooth_j_file = open('toothbrush.json', "r")
    data = json.loads(tooth_j_file.read())
    for i in data['emp_details']:
        print(i)
    tooth_j_file.close()
    
try:
    while True:
        if (GPIO.input(23)):
            stopwatch_time = setTimer(120)
                
            #if GPIO 23 is pressed again
                #write to json file: toothbrush.json the stopwatch time at the point of the second button press
        #if (GPIO.input(25)):
            #displayData()
except KeyboardInterrupt:
    pass
    
GPIO.cleanup()
