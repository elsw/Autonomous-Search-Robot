import RPi.GPIO as GPIO
import time
import numpy
from RangeData import RangeData

#Thie is a class designed to take readings from 1 SR04 sensor
#The class will add to the range_data array when it in running
#it will take readings in groups of 5 by default
#when the array is read it be operated on and then cleared for the next run
#the angle should be updated as it scans
class SR04_Single:

    #needs to sleep 3 seconds after initialising this
    def __init__(self,trig,echo,angle_offset, read_group_size = 7):
        self.read_group_size = read_group_size
        self.readings = numpy.zeros(read_group_size)
        self.pulse_start = 0.0
        self.pulse_end = 0.0
        self.count = 0
        self.trig = trig
        self.echo = echo
        self.angle = 0
        self.range_data = []
        self.running = False
        self.angle_offset = angle_offset
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(1)
        GPIO.add_event_detect(self.echo, GPIO.BOTH, callback=self.callbackEcho)

    def setAngle(self,angle):
        self.angle = angle

    def getRangeData(self):
        return self.range_data
    def clearRangeData(self):
        self.range_data = []

    def start(self):
        self.running = True;
        self.__pulse()
    #finishes the current set of data and stops
    def stop(self):
        self.running = False;
    #internal use only
    #sends out single pulse
    def __pulse(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

    def cleanup(self):
        GPIO.cleanup()

    #internal use only
    #interrupt on echo GPIO pin
    def callbackEcho(self,channel):
        if(GPIO.input(self.echo)):
            #rising
            self.pulse_start = time.time()
        else:
            #falling
            self.pulse_end = time.time()
            pulse_duration = self.pulse_end - self.pulse_start
            self.readings[self.count] = pulse_duration * 17150
            if(self.count >= self.read_group_size - 1):
                self.range_data.append(RangeData(self.angle + self.angle_offset,numpy.median(self.readings)))
                self.count = 0
                if(self.running):
                    self.__pulse()
            else:
                self.count += 1
                self.__pulse()

if __name__ == "__main__":
    s = SR04_Single(17,27)
    print "reading..."
    s.start();
    time.sleep(2)
    s.stop()
    time.sleep(0.1)
    data = s.getRangeData()
    for i in range(0,len(data) - 1):
        print "Angle : " + str(data[i].angle)
        print "Distance:" + str(data[i].distance)
    print len(data)
    s.cleanup()

