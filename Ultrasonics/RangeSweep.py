import RPi.GPIO as GPIO
from threading import Thread
import Queue
import time
import numpy
GPIO.setmode(GPIO.BCM)

SERVO_ANGLE = 0
SERVO_DONE = True

TRIG = 17#was 23 
ECHO = 27#was 24

#perform a sweep of range readings until SERVO_DONE is true
# assumes GPIO pins are already set up
#is blocking, should multithread this function for each ranger
# trig_pin      GPIO trigger pin
# echo_pin      GPIO echo pin
# angle_offset  The offset (in degrees) of the ranger
def RangeSweep(out_queue, trig_pin, echo_pin, angle_offset, READINGS=7):
  range_data = []
  readings = numpy.zeros(READINGS)
  
  while True:
    if(SERVO_DONE):
      break;
    angle = SERVO_ANGLE
    
    for j in range(0,READINGS- 1):
      GPIO.output(TRIG, True)
      time.sleep(0.00001)
      GPIO.output(TRIG, False)

      while GPIO.input(ECHO)==0:
        pulse_start = time.time()  #sometimes gets stuck here

      while GPIO.input(ECHO)==1:
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start

      readings[j] = pulse_duration * 17150
    range_data.append(RangeData(angle + angle_offset, numpy.median(readings)))
  out_queue.put(range_data)
  return 0

class RangeData:
  def __init__(self,angle,distance):
    self.angle = angle
    self.distance = distance

if __name__ == "__main__":
  print "Distance Measurement In Progress"

  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)

  GPIO.output(TRIG, False)
  print "Waiting For Sensor To Settle"
  time.sleep(2)
  print "reading..."
   
  queue1 = Queue.Queue()
  ranger1 = Thread( target=RangeSweep, args=(queue1,17,27,-120))

  SERVO_DONE = False
  ranger1.start()
  for i in range(0,19):
    SERVO_ANGLE = i * 10;
    time.sleep(0.1)
  SERVO_DONE = True
  ranger1_data = queue1.get()

  for i in range(0,len(ranger1_data) - 1):
    print "Angle : " + str(ranger1_data[i].angle)
    print "Distance:" + str(ranger1_data[i].distance)


  GPIO.cleanup()



