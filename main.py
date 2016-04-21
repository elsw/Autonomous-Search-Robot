#from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.RangeSweep import RangeSweep
from Ultrasonics.StepSweep import StepSweep
from Ultrasonics.RangeSweep import RangeSweep
from Ultrasonics.RangeData import RangeData
from Mapping.Mapping import Mapping
from Mapping.Navigation import Navigation
from Motor_Driver.MotorDriver import MotorDriver
from Servo_Driver.ServoDriver import ServoDriver
import time
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO



if __name__ == "__main__":
    #pwm = PWM(0x40)
    #pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    #pwm = PWM(0x40, debug=True)
    servoDriver = ServoDriver()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.init()
    m = Mapping(screen);
    print "setting up rangers"
    r = StepSweep(servoDriver)
    motor = MotorDriver()
    nav = Navigation(motor,screen)

    running = True
    wait_for_results = False

    r.start()
    
    print "reading..."
    while running:
        if wait_for_results:
            time.sleep(0.02)
            if r.isDone():
                rangeData = r.getRangeData()
                #ranging is done,update graphs
                screen.fill((255,255,255))
                m.addRangeData(rangeData)

                
                #pre move renders
                m.drawVertex()
                nav.calculateGaps(rangeData)
                nav.draw(0,0,m.getPosition(),m.getRotation())
        
                m.updatePosition(nav.getLastMovement())

                #post move renders
                #m.drawPosition()

                pygame.display.flip()

                time.sleep(5)
                
                nav.drive()
                wait_for_results = False
        else:
            #start new ranging
            print "new ranging..."
            r.servoToStart()
            time.sleep(0.7)
            rangeData = r.fullRange()
            wait_for_results = True

        for event in pygame.event.get():
            if event.type == QUIT:
                wait_for_input = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    r.cleanup()
    #wait for threads to end
    r.kill()
    r.join()
    pygame.quit()
    GPIO.cleanup()
