import RPi.GPIO as GPIO
import time
import numpy
from RangeData import RangeData
from threading import Thread

#Thie is a class designed to take readings from 1 SR04 sensor
#The class will add to the range_data array when it in running
#it will take readings in groups of 5 by default
#when the array is read it be operated on and then cleared for the next run
#the angle should be updated as it scans
class SR04_read(Thread):

    #needs to sleep 3 seconds after initialising this
    def __init__(self,trig,echo,read_buffer_length = 10, wait_time = 0.02):
        super(SR04_read, self).__init__()
        self.read_buffer_length = read_buffer_length
        self.read_buffer = numpy.zeros(read_buffer_length)
        self.pulse_start = 0.0
        self.pulse_end = 0.0
        self.buffer_head = 0
        self.trig = trig
        self.echo = echo
        self.running = False
        self.debug = False
        self.wait_time = wait_time # wait time between readings
        self.debug = False
        
        self.stop = False
        self.reading = False
        self.waiting_for_echo = False
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(1)
        GPIO.add_event_detect(self.echo, GPIO.BOTH, callback=self.callbackEcho)

    def run(self):
        while True:
            time.sleep(0.02) #free up other threads
            if self.stop:
                return 0
            while self.reading:
                self.__pulse()
                self.waiting_for_echo = True
                #wait for a minimum of wait_time
                time.sleep(self.wait_time)
                #wait for the echo (if it hasnt already happened)
                while self.waiting_for_echo:
                    time.sleep(0.01)
            

    def getRangeData(self):
        return self.read_buffer
    def clearRangeData(self):
        self.read_buffer = numpy.zeros(self.read_buffer_length)

    def startReading(self):
        self.reading = True

    def stopReading(self):
        self.reading = False
    
    def kill(self):
        self.stop = True

        
    #internal use only
    #sends out single pulse
    def __pulse(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

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
            self.read_buffer[self.buffer_head] = pulse_duration * 17150
            if self.debug:
                print pulse_duration * 17150
            self.buffer_head = self.buffer_head + 1
            if self.buffer_head >= self.read_buffer_length:
                self.buffer_head = 0
            self.waiting_for_echo = False


if __name__ == "__main__":
    s = SR04_read(17,27)
    time.sleep(2)
    s.debug = True
    print "reading..."
    s.start();
    s.startReading()
    time.sleep(2)
    s.stopReading()
    s.kill()
    s.join()
    data = s.getRangeData()
    for i in range(0,len(data) - 1):
        print data[i]
    GPIO.cleanup()

