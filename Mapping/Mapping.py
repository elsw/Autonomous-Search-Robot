from Ultrasonics.RangeData import RangeData
import pygame
import math

class Mapping:
    def __init__(self,screen):
        self.screen = screen
        self.locX = 350
        self.locY = 350
        self.rotation = 0
        self.cmPerPix = 1
        self.gap_data = []
        self.vertexData = []
        self.path = []
        #first path point is always start point
        self.path.append(PathPoint(self.locX,self.locY))
        
    def addRangeData(self,rangeData):
        for r in rangeData:
            angle = r.angle - 90 + self.rotation
            x = self.locX + r.distance *self.cmPerPix* math.cos(math.radians(angle))
            y = self.locY + r.distance *self.cmPerPix* math.sin(math.radians(angle))
            self.vertexData.append(Vertex(int(x),int(y))) #add vertex with default probability
    
    def drawVertex(self):
        
        self.__drawMap()

    def getPosition(self):
        return (self.locX,self.locY)

    def updatePosition(self,movedRotDis):
        rot_cm = movedRotDis[1] * 100 #convert m to cm
        self.rotation = self.rotation - movedRotDis[0]
        if self.rotation > 360:
            self.rotation = self.rotation - 360
        if self.rotation < 0:
            self.rotation = self.rotation + 360
            
        self.locX = self.locX + rot_cm *self.cmPerPix* math.cos(math.radians(self.rotation - 90))
        self.locY = self.locY + rot_cm *self.cmPerPix* math.sin(math.radians(self.rotation - 90))

        self.path.append(PathPoint(int(self.locX),int(self.locY)))
        
    def drawPosition(self):
        pygame.draw.circle(self.screen,(0,0,255),(int(self.locX),int(self.locY)), 5,0)
        lineX = self.locX + 15.0 * math.cos(math.radians(self.rotation - 90))
        lineY = self.locY + 15.0 * math.sin(math.radians(self.rotation - 90))
        pygame.draw.line(self.screen,(0,0,255),(int(self.locX),int(self.locY)),(int(lineX),int(lineY)),3)

        for i in range(1,len(self.path)):
            pygame.draw.line(self.screen,(255,0,255),(self.path[i].x,self.path[i].y),(self.path[i-1].x,self.path[i-1].y),2)
    
    def drawVertex(self):
        pygame.draw.circle(self.screen,(255,0,0),(int(self.locX),int(self.locY)), 100 *self.cmPerPix, 1)
        pygame.draw.circle(self.screen,(255,0,0),(int(self.locX),int(self.locY)), 200 *self.cmPerPix, 1)

        for vertex in self.vertexData:
            self.__drawDot(vertex.getX(),vertex.getY())
    
    def __drawDot(self,x,y):
        pygame.draw.circle(self.screen,(0,0,0),(x,y), 5,0)
        
class Vertex:
    def __init__(self,x,y,p = 0.5):
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
    

class PathPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
