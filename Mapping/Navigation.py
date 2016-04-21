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
        #self.locX = 350
        #self.locY = 350
        self.lastRotation = 0.0
        self.lastDistance = 0.0
        self.chosenGap = None
        self.distanceFromLeft = 0 # in cm


    def drive(self):
        if len(self.gap_data) > 0:
            self.motorDriver.left(-self.lastRotation)
            self.motorDriver.forward(self.lastDistance)
            
    def draw(self,offset,zoom,pos,rot):
        for gap in self.gap_data:
            posLeft = gap.getLeftPos(rot)
            posRight = gap.getRightPos(rot)
            leftx = int(pos[0] + posLeft[0])
            lefty = int(pos[1] - posLeft[1])
            rightx = int(pos[0] + posRight[0])
            righty = int(pos[1] - posRight[1])
            if gap == self.chosenGap:
                pygame.draw.line(self.screen,[255,0,0],(leftx,lefty),(rightx,righty),2)
            else:
                pygame.draw.line(self.screen,[0,255,0],(leftx,lefty),(rightx,righty),2)

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

        if len(self.gap_data) > 0:
            self.chosenGap = self.__chooseGap(self.gap_data)
            self.lastRotation = self.chosenGap.getAngleToDisFromLeft(self.distanceFromLeft)
            #self.lastRotation = self.chosenGap.getCenterAngle()
            #print "rotation:"
            #print self.lastRotation
            self.lastDistance = 0.5
        else:
            self.lastRotation = 0
            self.lastDistance = 0

                

    def __chooseGap(self,gapData):
        targetAngle = -30
        bestIndex = 0
        bestAngle = 10000
        #just choose most nearest facing atm
        for i in range(0,len(gapData)):
            print gapData[i].getCenterAngle()
            if abs(targetAngle - gapData[i].getCenterAngle()) < bestAngle:
                bestAngle = targetAngle - gapData[i].getCenterAngle()
                bestIndex = i
            if abs(targetAngle - (gapData[i].getCenterAngle()-360)) < bestAngle:
                bestAngle = targetAngle - gapData[i].getCenterAngle()
                bestIndex = i
        #print gapData[bestIndex].getCenterAngle()
        return gapData[bestIndex]

class GapData:
    def __init__(self,rangeDataLeft,rangeDataRight, cmPerPix = 1):
        self.rangeDataLeft = rangeDataLeft
        self.rangeDataRight = rangeDataRight
        self.cmPerPix = cmPerPix
        

    #optional position of robot
    def getLeftPos(self, rot = 0):
        loc = []
        # calculate X
        loc.append(int(self.rangeDataLeft.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataLeft.angle - 90 + rot))))
        #calcula+e
        loc.append(int(self.rangeDataLeft.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataLeft.angle + 90 + rot))))
        return loc

    def getRightPos(self, rot = 0):
        loc = []
        # calculate X
        loc.append(int(self.rangeDataRight.distance *self.cmPerPix* math.cos(math.radians(self.rangeDataRight.angle - 90 + rot))))
        #calculate Y 
        loc.append(int(self.rangeDataRight.distance *self.cmPerPix* math.sin(math.radians(self.rangeDataRight.angle + 90 + rot))))
        return loc


    #angle to inpolatated point using distance from the laft hand side
    def getAngleToDisFromLeft(self,distance):
        if(self.getGapSize() / 2 < distance):
            return self.getCenterAngle()
        else:
            left = self.getLeftPos()
            right = self.getRightPos()
            p = float(distance) / float(self.getGapSize())
            x = left[0] + (float(right[0] - left[0])*p)
            y = left[1] + (float(right[1] - left[1])*p)

            angle = math.degrees(math.atan(float(x)/float(y)))
            #y scale is upside down so angle will come out upside down
            #print 180 + angle
            if y < 0:
                angle = angle + 180
            return angle
                                                                            
    def getCenterAngle(self):
        mid = self.getMidPoint()
        angle = math.degrees(math.atan(float(mid[0])/float(mid[1])))
        if mid[1] < 0:
            angle = angle + 180
        return angle

    def getMidPoint(self):
        left = self.getLeftPos()
        right = self.getRightPos()
        xMid = left[0] + (float(right[0] - left[0])*0.5)
        yMid = left[1] + (float(right[1] - left[1])*0.5)
        return [xMid,yMid]

    def getGapSize(self):
        left = self.getLeftPos()
        right = self.getRightPos()
        dis = math.sqrt(math.pow(right[0] - left[0],2) + math.pow(right[1] - left[1],2))
        return dis
        
