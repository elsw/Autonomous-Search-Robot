import time
import sys
import RPi.GPIO as GPIO


class MotorDriver:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.leftPinForward=6
        self.leftPinBackward=5
        self.rightPinForward=13
        self.rightPinBackward=19
        self.turn90 = 0.7   #time for a 90 degree turn
        self.meterForward = 5 #time for 1 meter forward
        
        GPIO.setup(self.leftPinForward,GPIO.OUT)
        GPIO.setup(self.leftPinBackward,GPIO.OUT)
        GPIO.setup(self.rightPinForward,GPIO.OUT)
        GPIO.setup(self.rightPinBackward,GPIO.OUT)
    
    def forward(self,distance):
        if distance > 0:
            GPIO.output(self.leftPinForward, GPIO.HIGH)
            GPIO.output(self.rightPinForward, GPIO.HIGH)
            time.sleep(self.meterForward * distance)
            GPIO.output(self.leftPinForward, GPIO.LOW)
            GPIO.output(self.rightPinForward, GPIO.LOW)
        else:
            GPIO.output(self.leftPinBackward, GPIO.HIGH)
            GPIO.output(self.rightPinBackward, GPIO.HIGH)
            time.sleep(self.meterForward * -distance)
            GPIO.output(self.leftPinBackward, GPIO.LOW)
            GPIO.output(self.rightPinBackward, GPIO.LOW)

    def left(self,degrees):
        if degrees > 0:
            GPIO.output(self.leftPinBackward, GPIO.HIGH)
            GPIO.output(self.rightPinForward, GPIO.HIGH)
            time.sleep(self.turn90 * (float(degrees)/90.0))
            GPIO.output(self.leftPinBackward, GPIO.LOW)
            GPIO.output(self.rightPinForward, GPIO.LOW)
        else:
            GPIO.output(self.leftPinForward, GPIO.HIGH)
            GPIO.output(self.rightPinBackward, GPIO.HIGH)
            time.sleep(self.turn90 * (float(-degrees)/90.0))
            GPIO.output(self.leftPinForward, GPIO.LOW)
            GPIO.output(self.rightPinBackward, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    m = MotorDriver()
    #m.forward(0.3)
    #m.forward(-0.2)
    m.left(-90)
    #m.left(-90)

    m.cleanup()
    
