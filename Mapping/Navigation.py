from Motor_Driver.MotorDriver import MotorDriver
import pygame
import math

class Navigation:
    def __init__(self,motorDriver,screen):
        self.motorDriver = motorDriver
        self.screen = screen        
        self.driveStep = 0.5#aim for driving 0.5 meter berfore anther range map
        self.gap_data = []
        self.readLimit = 200 #ignore everything over 200 cm
        self.locX = 350
        self.locY = 350
        self.lastRotation = 0.0
        self.lastDistance = 0.0
        self.chosenGap = None


    def drive(self):
        if len(self.gap_data) > 0:
            self.motorDriver.left(-self.chosenGap.getCenterAngle())
            self.motorDriver.forward(0.5)
            self.lastRotation = -self.chosenGap.getCenterAngle()
            self.lastDistance = 0.5
            
    def draw(self,offset,zoom,pos,rot):
        for gap in self.gap_data:
            posLeft = gap.getLeftPos(pos,rot)
            posRight = gap.getRightPos(pos,rot)
            pygame.draw.line(self.screen,[0,255,0],(int(posLeft[0]),int(posLeft[1])),(int(posRight[0]),int(posRight[1])),2)

    def getLastMovement(self):
        return (self.lastRotation,self.lastDistance)

    def calculateGaps(self,rangeData):
        minGapAngle = 20 #at least 20 degrees to be considered a gap
        self.gap_data = []
        lastAngle = 0.0
        lastIndex = 0
        #find last angle before 360
        for n in range(0, len(rangeData)):
            i = -n + (len(rangeData) - 1)
            if(rangeData[i].distance < self.readLimit):
                lastAngle = rangeData[i].angle - 360
                lastIndex = i
                break

        #run through all points finding gaps
        for i in range(0,len(rangeData)):
            if rangeData[i].distance < self.readLimit:
                if rangeData[i].angle - lastAngle > minGapAngle:
                    self.gap_data.append(GapData(rangeData[lastIndex],rangeData[i]))
                lastAngle = rangeData[i].angle
                lastIndex = i

        if self.gap_data > 0:
            self.chosenGap = self.__chooseGap(self.gap_data)
            self.lastRotation = -self.chosenGap.getCenterAngle()
            self.lastDistance = 0.5
        else:
            self.lastRotation = 0
            self.lastDistance = 0

                

    def __chooseGap(self,gapData):
        bestIndex = 0
        bestAngle = 10000
        #just choose most nearest facing atm
        for i in range(0,len(gapData)):
            if abs(gapData[i].getCenterAngle()) < bestAngle:
                bestAngle = gapData[i].getCenterAngle()
                bestIndex = i
        return gapData[bestIndex]

class GapData:
    def __init__(self,rangeDataLeft,rangeDataRight, cmPerPix = 1):
        self.rangeDataLeft = rangeDataLeft
        self.rangeDataRight = rangeDataRight
        self.cmPerPix = cmPerPix
        

    #optional position of robot
    def getLeftPos(self,pos = (0,0),rot = 0):
        loc = []
        # calculate X
        loc.append(pos[0]+ int(self.rangeDataLeft.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataLeft.angle - 90 + rot))))
        #calculate Y
        loc.append(pos[1] + int(self.rangeDataLeft.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataLeft.angle - 90 + rot))))
        return loc

    def getRightPos(self,pos = (0,0),rot = 0):
        loc = []
        # calculate X
        loc.append(pos[0] + int(self.rangeDataRight.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataRight.angle - 90 + rot))))
        #calculate Y
        loc.append(pos[1] + int(self.rangeDataRight.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataRight.angle - 90 + rot))))
        return loc

                                                                        
    def getCenterAngle(self):
        left = 0.0
        right = 0.0
        if self.rangeDataRight.angle - self.rangeDataLeft.angle < 0:
            #in this case the gap is over the 360 boundry
            right = self.rangeDataRight.angle
            left = self.rangeDataLeft.angle - 360
        else:
            #other wise not over the 360 boundry
            right = self.rangeDataRight.angle
            left = self.rangeDataLeft.angle
        return right - ((right - left)/2)

    def getGapSize(self):
        left = self.getLeftPos()
        right = self.getRightPos()
        return sqrt(sqr(right[0] - left[0]) + sqr(right[1] - left[1]))
        
