from Ultrasonics.RangeData import RangeData
import pygame
import math

class Mapping:
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.locX = 250
        self.locY = 250

    def rawMap(self,rangeData):
        self.screen.fill((255,255,255))
        pygame.draw.circle(self.screen,(0,0,255),(self.locX,self.locY), 5,0)
        for i in range(0,len(rangeData) - 1):
            angle = rangeData[i].angle - 90
            x = rangeData[i].distance *3* math.cos(math.radians(angle))
            y = rangeData[i].distance *3* math.sin(math.radians(angle))
            self.__drawDot(self.locX + int(x),self.locY + int(y))
        pygame.display.flip()

    def __drawDot(self,x,y):
        pygame.draw.circle(self.screen,(0,0,0),(x,y), 5,0)
        
