from Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
from Ultrasonics.RangeSweep import RangeSweep
from Mapping.Mapping import Mapping
import time
import pygame

running = True

if __name__ == "__main__":
    pwm = PWM(0x40)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    #pwm = PWM(0x40, debug=True)
    m = Mapping();
    print "setting up rangers"
    r = RangeSweep(pwm)
    
    print "reading..."
    while running:
        r.servoToStart()
        time.sleep(1)
        data = r.fullRange()
        m.rawMap(data)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
    
    #raw_input()
    pygame.quit()
    r.cleanup()
