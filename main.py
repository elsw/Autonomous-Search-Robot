from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.RangeSweep import RangeSweep
from Ultrasonics.StepSweep import StepSweep
from Ultrasonics.RangeData import RangeData
from Mapping.Mapping import Mapping
import time
import pygame
import RPi.GPIO as GPIO



if __name__ == "__main__":
    pwm = PWM(0x40)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    #pwm = PWM(0x40, debug=True)
    m = Mapping();
    print "setting up rangers"
    r = StepSweep(pwm)

    running = True
    wait_for_input = True
    
    print "reading..."
    while running:
        wait_for_input = True
        r.servoToStart()
        time.sleep(1)
        rangeData = r.fullRange()
        m.rawMap(rangeData)

        while wait_for_input:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        wait_for_input = False
    pygame.quit()
    GPIO.cleanup()
