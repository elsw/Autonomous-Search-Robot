from Ultrasonics.RangeData import RangeData
from Motor_Driver.MotorDriver import MotorDriver
import pygame
import math

class Mapping:
    def __init__(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((700, 700))
        self.locX = 350
        self.locY = 350
        self.cmPerPix = 1
        self.gap_data = []
        self.readLimit = 200 #ignore everything over 200 cm

    def rawMap(self,rangeData):
        self.screen.fill((255,255,255))
        self.__drawMap(rangeData)
        self.__calculateGaps(rangeData, True)
        pygame.display.flip()

    def __calculateGaps(self,rangeData, debug = False):
        minGapAngle = 20 #at least 20 degrees to be considered a gap
        self.gap_data = []
        lastAngle = 0.0
        finalIndex = 0
        #find last angle before 360
        for n in range(0, len(rangeData)):
            i = -n + (len(rangeData) - 1)
            if(rangeData[i].distance < self.readLimit):
                lastAngle = rangeData[i].angle - 360
                finalIndex = i
                break

        for i in range(0,len(rangeData)):
            if rangeData[i].distance < self.readLimit:
                if rangeData[i].angle - lastAngle > minGapAngle:
                    if i == 0:
                        self.gap_data.append(GapData(rangeData[finalIndex],rangeData[i],self.locX,self.locY))
                    else:
                        self.gap_data.append(GapData(rangeData[i - 1],rangeData[i],self.locX,self.locY))
                lastAngle = rangeData[i].angle
        if(debug):
            for gap in self.gap_data:
                pygame.draw.line(self.screen,[0,255,0],gap.getLeftPos(),gap.getRightPos(),2)
    
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
        
class GapData:
    def __init__(self,rangeDataLeft,rangeDataRight,locX = 0, locY = 0, cmPerPix = 1):
        self.rangeDataLeft = rangeDataLeft
        self.rangeDataRight = rangeDataRight
        self.cmPerPix = cmPerPix
        #optional position of robot
        self.locX = locX
        self.locY = locY

    def getLeftPos(self):                                              
        pos = []
        # calculate X
        pos.append(self.locX + int(self.rangeDataLeft.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataLeft.angle - 90))))
        #calculate Y
        pos.append(self.locY + int(self.rangeDataLeft.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataLeft.angle - 90))))
        return pos

    def getRightPos(self):                                              
        pos = []
        # calculate X
        pos.append(self.locX + int(self.rangeDataRight.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataRight.angle - 90))))
        #calculate Y
        pos.append(self.locY + int(self.rangeDataRight.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataRight.angle - 90))))
        return pos

                                                                    
    def getCenterAngle(self):
        left = 0.0
        right = 0.0
        if self.rangeDataRight - self.rangeDataLeft < 0:
            #in this case the gap is over the 360 boundry
            right = self.rangeDataRight.angle
            left = self.rangeDataLeft.angle - 360
        else:
            #other wise not over the 360 boundry
            right = self.rangeDataRight.angle
            left = self.rangeDataLeft.angle
        return right - ((right - left)/2)


        
