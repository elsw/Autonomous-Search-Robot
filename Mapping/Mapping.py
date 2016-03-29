from Ultrasonics.RangeData import RangeData
import pygame
import math

class Mapping:
    def __init__(self,screen):
        pygame.display.init()
        self.screen = screen
        self.locX = 350
        self.locY = 350
        self.rotation = 0
        self.cmPerPix = 1
        self.gap_data = []
        self.rangeData = []
        
    def addRangeData(self,rangeData):
        self.rangeData.extend(rangeData)
    
    def draw(self):
        self.screen.fill((255,255,255))
        self.__drawMap(self.rangeData)

    def getPosition(self):
        return (self.locX,self.locY)

    def updatePosition(self,movedRotDis):
        self.locX = self.locX + movedRotDis[1] *self.cmPerPix* math.cos(math.radians(movedRotDis[0]))
        self.locY = self.locY + movedRotDis[1] *self.cmPerPix* math.sin(math.radians(movedRotDis[0]))
        self.rotation = self.rotation + movedRotDis[0]
        if self.rotation > 360:
            self.rotation = self.rotation - 360
        if self.rotation < 0:
            self.rotation = self.rotation + 360

    
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
        
class Vertex(self,x,y,p = 0.5):
    self.x = x
    self.y = y
    self.p = p


    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getP(self):
        return self.p
    def setX(self,x):
        self.x = x
    def setY(self,y):
        self.y = y
    def setP(self,p):
        self.p = p
    


        
