import RPi.GPIO as GPIO
import time
import numpy
GPIO.setmode(GPIO.BCM)

TRIG = 17 
ECHO = 27

READINGS = 21

readings = numpy.zeros(READINGS)

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

while True:
  for j in range(0,READINGS- 1):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
      pulse_start = time.time()  #sometimes gets stuck here

    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    #distance = pulse_duration * 17150

    readings[j] = pulse_duration * 17150
    #distance = round(distance, 2)

    #print "Distance:",distance,"cm"

  print "Distance: ",numpy.median(readings)," cm"
GPIO.cleanup()
