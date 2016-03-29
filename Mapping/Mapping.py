from Ultrasonics.RangeData import RangeData
import pygame
import math

class Mapping:
    def __init__(self,screen):
        pygame.display.init()
        self.screen = screen
        self.locX = 350
        self.locY = 350
        self.cmPerPix = 1
        self.gap_data = []
        

    
    def rawMap(self,rangeData):
        self.screen.fill((255,255,255))
        self.__drawMap(rangeData)

    
    def __drawMap(self,rangeData):
        pygame.draw.circle(self.screen,(0,0,255),(self.locX,self.locY), 5,0)
        pygame.draw.circle(self.screen,(255,0,0),(self.locX,self.locY), 100 *self.cmPerPix, 1)
        pygame.draw.circle(self.screen,(255,0,0),(self.locX,self.locY), 200 *self.cmPerPix, 1)
        for r in rangeData:
            angle = r.angle - 90
            x = r.distance *self.cmPerPix* math.cos(math.radians(angle))
            y = r.distance *self.cmPerPix* math.sin(math.radians(angle))
            self.__drawDot(self.locX + int(x),self.locY + int(y))
    
    def __drawDot(self,x,y):
        pygame.draw.circle(self.screen,(0,0,0),(x,y), 5,0)
        



        
