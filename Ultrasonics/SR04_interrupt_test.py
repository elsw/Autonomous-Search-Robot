import RPi.GPIO as GPIO
import time
import numpy

GPIO.setmode(GPIO.BCM)

TRIG = 17 
ECHO = 27

READINGS = 3

pulse_start = 0.0
pulse_end = 0.0

#readings = numpy.zeros(READINGS)


def callbackEcho(channel):
    global pulse_start
    global pulse_end
    if(GPIO.input(ECHO)):
        #rising
        pulse_start = time.time()
    else:
        #falling
        pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        result = pulse_duration * 17150
        print result," cm"
    
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)



GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(1)
#GPIO.output(TRIG, True)
#time.sleep(0.00001)
#GPIO.output(TRIG, False)
#time.sleep(3)
GPIO.add_event_detect(ECHO, GPIO.BOTH, callback=callbackEcho)
time.sleep(3)
while True:
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    time.sleep(0.5)

GPIO.cleanup()
