from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.RangeSweep import RangeSweep
from Ultrasonics.StepSweep import StepSweep
from Ultrasonics.RangeData import RangeData
from Mapping.Mapping import Mapping
from Mapping.Navigation import Navigation
from Motor_Driver.MotorDriver import MotorDriver
import time
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO



if __name__ == "__main__":
    pwm = PWM(0x40)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    #pwm = PWM(0x40, debug=True)
    screen = pygame.display.set_mode((700, 700))
    m = Mapping(screen)
    motor = MotorDriver()
    nav = Navigation(motor,screen)
    print "setting up rangers"
    r = StepSweep(pwm)

    running = True
    wait_for_input = True
    
    print "reading..."
    while running:
        wait_for_input = True
        r.servoToStart()
        time.sleep(1)
        rangeData = []
        rangeData.append(RangeData(10,120))
        rangeData.append(RangeData(100,90))
        rangeData.append(RangeData(115,160))
        rangeData.append(RangeData(200,100))
        rangeData.append(RangeData(235,140))
        rangeData.append(RangeData(240,120))
        rangeData.append(RangeData(250,170))
        
        m.addRangeData(rangeData)

        m.draw()

        nav.draw(0,0,m.getPosition())
        
        pygame.display.flip()

        nav.drive(rangeData)
        m.updatePosition(nav.getLastMovement())
        

        while wait_for_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    wait_for_input = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wait_for_input = False
                    if event.key == pygame.K_ESCAPE:
                        wait_for_input = False
                        running = False

    r.cleanup()
    pygame.quit()
    GPIO.cleanup()
