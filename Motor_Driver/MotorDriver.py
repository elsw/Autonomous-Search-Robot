import time
import sys
import RPi.GPIO as GPIO


class MotorDriver:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.leftPinForward=5
        self.leftPinBackward=6
        self.rightPinForward=13
        self.rightPinBackward=19
        self.90Turn = 0.5   #time for a 90 degree turn
        self.meterForward = 3 #time for 1 meter forward

    
    def forward(self,distance):
        if distance > 0:
            GPIO.output(self.leftPinForward, GPIO.HIGH)
            GPIO.output(self.rightPinForward, GPIO.HIGH)
            time.sleep(time)
            GPIO.output(self.leftPinForward, GPIO.LOW)
            GPIO.output(self.rightPinForward, GPIO.LOW)
        else:
            GPIO.output(self.leftPinBackward, GPIO.HIGH)
            GPIO.output(self.rightPinBackward, GPIO.HIGH)
            time.sleep(time)
            GPIO.output(self.leftPinBackward, GPIO.LOW)
            GPIO.output(self.rightPinBackward, GPIO.LOW)

    def left(self,degrees):
        if degrees > 0:
            GPIO.output(self.leftPinBackward, GPIO.HIGH)
            GPIO.output(self.rightPinForward, GPIO.HIGH)
            time.sleep(time)
            GPIO.output(self.leftPinBackward, GPIO.LOW)
            GPIO.output(self.rightPinForward, GPIO.LOW)
        else:
            GPIO.output(self.leftPinForward, GPIO.HIGH)
            GPIO.output(self.rightPinBackward, GPIO.HIGH)
            time.sleep(time)
            GPIO.output(self.leftPinForward, GPIO.LOW)
            GPIO.output(self.rightPinBackward, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
