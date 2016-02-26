from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.RangeSweep import RangeSweep
import time

if __name__ == "__main__":
    pwm = PWM(0x40)
    #pwm = PWM(0x40, debug=True)
    print "setting up rangers"
    r = RangeSweep(pwm)
    r.servoToStart()
    time.sleep(1)
    print "reading..."
    data = r.fullRange()
    for i in range(0,len(data) - 1):
        print "Angle : " + str(data[i].angle)
        print "Distance:" + str(data[i].distance)

    r.cleanup()
