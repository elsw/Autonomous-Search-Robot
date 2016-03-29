import time
from SR04_single import SR04_Single

class RangeSweep:
    def __init__(self,pwm):
        self.ranger1 = SR04_Single(17,27,0)
        self.ranger2 = SR04_Single(23,24,120)
        self.ranger3 = SR04_Single(10,9,-120)
        time.sleep(3)
        self.pwm = pwm
        #pwm = PWM(0x40, debug=True)
        self.start_deg_pwm = 620 #0 degrees
        self.end_deg_pwm = 275   #120 degrees
        self.channel = 0
        self.time = 6 #sweep time in seconds
        self.steps = 120 #number of steps in sweep
        self.angle = 120 #amount of angle sweeped

    def fullRange(self):
        range_data = []

        
        #start each ranger slighty offset on time
        self.ranger1.start()
        time.sleep(0.05)
        #self.ranger2.start()
        time.sleep(0.05)
        #self.ranger3.start()
        time.sleep(0.2)
        
        #control the servo and update the angles
        diff = self.start_deg_pwm - self.end_deg_pwm
        for i in range(0,self.steps):
            self.pwm.setPWM(self.channel,0,self.start_deg_pwm - (int((float(i)/float(self.steps))*float(diff))))
            
            angle = (float(i)/float(self.steps))*float(self.angle)
            self.ranger1.setAngle(angle)
            self.ranger2.setAngle(angle)
            self.ranger3.setAngle(angle)
            time.sleep(float(self.time)/float(self.steps))

        self.ranger1.stop()
        self.ranger2.stop()
        self.ranger3.stop()
        #wait for rangers to finish final reading
        time.sleep(0.1)
        range_data.extend(self.ranger1.getRangeData())
        range_data.extend(self.ranger2.getRangeData())
        range_data.extend(self.ranger3.getRangeData())
        self.ranger1.clearRangeData();
        self.ranger2.clearRangeData();
        self.ranger3.clearRangeData();

        return range_data

    def servoToStart(self):
        self.pwm.setPWM(self.channel,0,self.start_deg_pwm)
    
    def cleanup(self):
        #self.ranger1.cleanup()
        #self.ranger2.cleanup()
        self.ranger3.cleanup()



        
        
