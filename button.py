import RPi.GPIO as GPIO
import time
from signal import pause
import json
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

activeBrushing = False
'''
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
            return stopwatch_display
    print('Good job brushing!')
'''
def displayData():
        os.system("python /home/group6/MagicMirror/modules/MMM-PythonPrint/toothbrush.py --show")
try:
    while True:
        if (GPIO.input(23)):
                os.system("echo 'a' > /dev/rfcomm1")
                time.sleep(0.1)
                if activeBrushing == True:
                    # Stop the timer, get timer value
                    brushtime = time.time() - start_time 
                    brushtime/= 60
                    # Convert value to minutes (as a float)
                    # call toothbrush --store [time]
                    #displayData(stopwatch_display)
                    #print(stopwatch_display)
                    stopwatch_data = ("python /home/group6/MagicMirror/modules/MMM-PythonPrint/toothbrush.py --store ")+(str)(brushtime)
                    print("STORING: ", stopwatch_data)
                    os.system(stopwatch_data)
                    # set activeBrushing to false
                    # delay
                    time.sleep(0.2)
                    # run toothbrush --show
                    #print ('\033[2J')
                    os.system("python /home/group6/MagicMirror/modules/MMM-PythonPrint/toothbrush.py --show")
                    activeBrushing = False
                elif activeBrushing == False:
                    start_time = time.time()
                    activeBrushing = True
                    time.sleep(1)
                    #setTimer(120)
                    # switch activeBrushing to True
                    # start timer
                else:
                    print("Error")
                
        '''
        if (GPIO.input(23) and not False):
            setTimer(120)
            if (GPIO.input(23)):
                state_on = False
        
            #displayData()
            #if GPIO 23 is pressed again
                #write to json file: toothbrush.json the stopwatch time at the point of the second button press
        #if (GPIO.input(25)):
            #displayData()
        '''    
except KeyboardInterrupt:
    pass
    
GPIO.cleanup()
