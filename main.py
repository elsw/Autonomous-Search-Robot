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
    pygame.display.init()
    m = Mapping(screen);
    print "setting up rangers"
    r = StepSweep(pwm)
    motor = MotorDriver()
    nav = Navigation(motor,screen)

    running = True
    wait_for_input = True
    
    print "reading..."
    while running:
        screen.fill((255,255,255))
        r.servoToStart()
        time.sleep(1)
        rangeData = r.fullRange()
        m.addRangeData(rangeData)

        #pre move renders
        m.drawVertex()
        nav.calculateGaps(rangeData)
        print m.getPosition()
        nav.draw(0,0,m.getPosition())
        
        m.updatePosition(nav.getLastMovement())

        #post move renders
        m.drawPosition()
        

        pygame.display.flip()
        
        nav.drive()
        m.updatePosition(nav.getLastMovement())
        
        for event in pygame.event.get():
            if event.type == QUIT:
                wait_for_input = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    r.cleanup()
    pygame.quit()
    GPIO.cleanup()
