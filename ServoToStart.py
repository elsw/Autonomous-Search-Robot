from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.StepSweep import StepSweep
from Servo_Driver.ServoDriver import ServoDriver
import time

if __name__ == "__main__":
    #pwm = PWM(0x40)
    #pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    #pwm = PWM(0x40, debug=True)
    servoDriver = ServoDriver()
    r = StepSweep(servoDriver)
    r.servoToStart()
    time.sleep(0.5)
    r.cleanup()
