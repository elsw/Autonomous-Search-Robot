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



def draw():
    screen.fill((255,255,255))
    m.drawVertex(offset)
    nav.draw(offset,0,m.getLastPosition(),m.getLastRotation())
    m.drawPosition()
    pygame.display.flip()
    
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
    offset = (0,0)

    r.start()

    r.servoToStart()
    time.sleep(0.7)
    
    print "reading..."
    while running:
        if wait_for_results:
            time.sleep(0.02)
            if r.isDone():
                rangeData = r.getRangeData()
                
                #ranging is done,update graphs
                m.addRangeData(rangeData)
                nav.calculateGaps(rangeData)
                m.updatePosition(nav.getLastMovement())
                draw()
                r.servoToStart()
                nav.drive()
                wait_for_results = False
        else:
            #start new ranging
            print "new ranging..."
            rangeData = r.fullRange()
            wait_for_results = True

        for event in pygame.event.get():
            if event.type == QUIT:
                wait_for_input = False
                running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    m.toggleEnableP()
                    draw()
                if event.key == pygame.K_UP:
                    offset[0] = offset[0] - 50
                    draw()
                if event.key == pygame.K_DOWN:
                    offset[0] = offset[0] + 50
                    draw()
                if event.key == pygame.K_LEFT:
                    offset[0] = offset[1] - 50
                    draw()
                if event.key == pygame.K_RIGHT:
                    offset[0] = offset[0] + 50
                    draw()
    r.cleanup()
    #wait for threads to end
    r.kill()
    r.join()
    pygame.quit()
    GPIO.cleanup()
