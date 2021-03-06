import time
import numpy
from SR04_read import SR04_read
from RangeData import RangeData
from threading import Thread

#this class performs a full 360 range scan
#call fullRange() and wait for done() to be high then

class StepSweep(Thread):
    def __init__(self,servoDriver):
        super(StepSweep, self).__init__()
        #self.pwm = pwm
        self.servoDriver = servoDriver
        self.pwm_channel = 0
        #self.start_deg_pwm = 620 #0 degrees
        #self.end_deg_pwm = 275   #120 degrees

        self.step_time = 0.8 #sweep time in seconds
        self.inter_step_time = 0.35 #servo moving time
        self.steps = 15  #number of steps in sweep
        self.angle_sweep = 120 #amount of angle sweeped
        #if readings disagree by more than this (in cm), the reading will be disregarded
        self.consistancyThreshold = 100 
        self.angle = 0.0
        
        time.sleep(3)
        self.ranger1 = SR04_read(17,27)
        self.ranger2 = SR04_read(23,24)
        self.ranger3 = SR04_read(10,9)

        self.ranger1.start()
        self.ranger2.start()
        self.ranger3.start()

        self.stop = False
        self.running = False
        self.done = False
        self.pause = False


    def run(self):
        while True:
            if self.stop:
                return 0
            if not self.running:
                time.sleep(0.02)
            else:
                while self.pause:
                    time.sleep(0.02)
                self.range_data = []
                #diff = self.start_deg_pwm - self.end_deg_pwm
                #self.ranger1.debug = True
                #self.ranger2.debug = True
                        
                for i in range(0,self.steps):
                    #self.pwm.setPWM(self.pwm_channel,0,self.start_deg_pwm -
                    #                (int((float(i)/float(self.steps))*float(diff))))
                    self.angle = float(i)/float(self.steps) * float(self.angle_sweep)
                    self.servoDriver.setAngle(self.angle)
                    time.sleep(self.inter_step_time)

                    #start each ranger offset from each other for less interfereance
                    self.ranger1.startReading()
                    time.sleep(float(self.ranger1.wait_time) / 3.0)
                    self.ranger2.startReading()
                    time.sleep(float(self.ranger2.wait_time) / 3.0)
                    self.ranger3.startReading()
                    time.sleep(float(self.ranger3.wait_time) / 3.0)
                    
                    time.sleep(self.step_time)
                    
                    self.ranger1.stopReading()
                    time.sleep(float(self.ranger1.wait_time) / 3.0)
                    self.ranger2.stopReading()
                    time.sleep(float(self.ranger2.wait_time) / 3.0)
                    self.ranger3.stopReading()
                    time.sleep(float(self.ranger3.wait_time) / 3.0)
                    
                    self.__collectData()

                    self.ranger1.clearRangeData()
                    self.ranger2.clearRangeData()
                    self.ranger3.clearRangeData()

                    if self.stop:
                        return 0
                    while self.pause:
                        time.sleep(0.02)
                
                self.range_data.sort(key=lambda x: x.angle)
                #for i in range(0,len(self.range_data)):
                #    print self.range_data[i].angle
                
                #stop after singe run through
                self.running = False
                self.done = True

    def fullRange(self):
        self.done = False
        self.running = True
        
    def isDone(self):
        return self.done
    
    def setPaused(self,paused):
        self.pause = paused
    def isPaused(self):
        return self.pause
    
    #make sure ranging is done before calling this
    def getRangeData(self):
        return self.range_data

    def kill(self):
        self.stop = True

    def servoToStart(self):
        self.servoDriver.setAngle(0)
        #self.pwm.setPWM(self.pwm_channel,0,self.start_deg_pwm)

    def __collectData(self):
        r1 = self.__getValue(self.ranger1.getRangeData())
        r2 = self.__getValue(self.ranger2.getRangeData())
        r3 = self.__getValue(self.ranger3.getRangeData())

        if r1 != 0:
            self.range_data.append(RangeData(self.angle,r1))
        if r2 != 0:
            self.range_data.append(RangeData(self.angle + 120,r2))
        if r3 != 0:
            self.range_data.append(RangeData(self.angle + 240,r3))

    #checks a set of data
    #if the data is reliable (all agree) returns average
    #otherwise signifying the data is unreliable
    #coded to size 10
    def __getValue(self,data):
        sorted_data = numpy.sort(data)
        #print sorted_data
        #find range of array ignoring top 2 and bottom 2 outliers
        nmin = 10000000
        nmax = -10000000
        for i in range(2,len(sorted_data) - 3):
            if data[i] > nmax:
                nmax = data[i]
            if data[i] < nmin:
                nmin = data[i]
        data_range = nmax - nmin
        if data_range > self.consistancyThreshold:
            return 0
        else:
            #print "average:"
            #print numpy.average(sorted_data[2:7])
            #print "\n"
            return numpy.average(sorted_data[2:7])

    def cleanup(self):
        self.ranger1.kill()
        self.ranger2.kill()
        self.ranger3.kill()
        #wait for threads to end
        self.ranger1.join()
        self.ranger2.join()
        self.ranger3.join()
            
        
        
