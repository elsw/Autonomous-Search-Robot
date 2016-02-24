import RPi.GPIO as GPIO
from threading import Thread,Event
from RangeData import RangeData
import Queue
import time
import numpy

class RangeSweep:
  def __init__(self):
    self.SERVO_DONE = Event()
    self.SERVO_ANGLE = 0.0
    self.__trig1 = 17
    self.__echo1 = 27
    self.__trig2 = 23
    self.__echo2 = 24
    self.__trig3 = 10
    self.__echo3 = 9
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(self.__trig1,GPIO.OUT)
    GPIO.setup(self.__echo1,GPIO.IN)
    GPIO.setup(self.__trig2,GPIO.OUT)
    GPIO.setup(self.__echo2,GPIO.IN)
    GPIO.setup(self.__trig3,GPIO.OUT)
    GPIO.setup(self.__echo3,GPIO.IN)

    GPIO.output(self.__trig1, False)
    GPIO.output(self.__trig2, False)
    GPIO.output(self.__trig3, False)
    #wait for sensors to settle
    time.sleep(2)

  #performs full 360 range sweep using 3 SR04 and a servo
  def fullSweep(self):
    range_data = []

    sweep1 = single_sweep(self.SERVO_DONE,range_data,17,27,0);
    sweep2 = single_sweep(self.SERVO_DONE,range_data,23,24,120);
    sweep3 = single_sweep(self.SERVO_DONE,range_data,10,9,-120);
    
    sweep1.start()
    sweep2.start()
    #sweep3.start()
    
    for i in range(0,12):
      self.SERVO_ANGLE = i * 10;
      time.sleep(0.1)
      
    self.SERVO_DONE.set();
    
    sweep1.join()
    sweep2.join()
    #sweep3.join()

    self.SERVO_DONE.clear()
    return range_data
  
  def cleanup(self):
    GPIO.cleanup()

class single_sweep(Thread):

  def __init__(self,servo_done,range_data, trig_pin, echo_pin, angle_offset, READINGS=7):
    super(single_sweep, self).__init__()
    self.trig_pin = trig_pin
    self.echo_pin = echo_pin
    self.angle_offset = angle_offset
    self.READINGS = READINGS
    self.servo_done = servo_done
    self.range_data = range_data
    
  #perform a sweep of range readings until SERVO_DONE is true
  # assumes GPIO pins are already set up
  #is blocking, should multithread this function for each ranger
  # trig_pin      GPIO trigger pin
  # echo_pin      GPIO echo pin
  # angle_offset  The offset (in degrees) of the ranger
  def run(self):
    
    readings = numpy.zeros(self.READINGS)
      
    while not self.servo_done.isSet():
        
       angle = 0
        
       for j in range(0,self.READINGS- 1):
         GPIO.output(self.trig_pin, True)
         time.sleep(0.00001)
         GPIO.output(self.trig_pin, False)
         
         while GPIO.input(self.echo_pin)==0:
           pulse_start = time.time()  #sometimes gets stuck here

         while GPIO.input(self.echo_pin)==1:
           pulse_end = time.time()

         pulse_duration = pulse_end - pulse_start
         readings[j] = pulse_duration * 17150
       print numpy.median(readings)
       self.range_data.append(RangeData(angle + self.angle_offset, numpy.median(readings)))
    return 0

  

if __name__ == "__main__":
  print "init range sweep"
  r = RangeSweep()
  print "reading data"
  data = r.fullSweep()
  print "data out:"
  for i in range(0,len(data) - 1):
    print "Angle : " + str(data[i].angle)
    print "Distance:" + str(data[i].distance)

  r.cleanup()

