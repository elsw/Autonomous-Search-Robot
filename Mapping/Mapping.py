from Ultrasonics.RangeData import RangeData
import pygame
import math

class Mapping:
    def __init__(self,screen):
        self.screen = screen
        self.locX = 350
        self.locY = 350
        self.lastLocX = 350
        self.lastLocY = 350
        self.rotation = 0
        self.lastRotation = 0
        self.cmPerPix = 1
        self.gap_data = []
        self.vertexData = []
        self.path = []
        #first path point is always start point
        self.path.append(PathPoint(self.locX,self.locY))
        self.enableP = True

        
        self.rangeLimit = 200 #this is the max range that readings are tacken as true
        self.agreeRange = 15  #range that considers that 2 points "agree", will increase propability of
                              #vertices that are in this range of each other
                
    def addRangeData(self,rangeData):
        for r in rangeData:
            angle = r.angle - 90 + self.rotation
            x = self.locX + r.distance *self.cmPerPix* math.cos(math.radians(angle))
            y = self.locY + r.distance *self.cmPerPix* math.sin(math.radians(angle))
            self.__addVertex(Vertex(int(x),int(y)))
        self.__fuseVertexData()
    

    def getPosition(self):
        return (self.locX,self.locY)
    def getLastPosition(self):
        return (self.lastLocX,self.lastLocY)
    def getRotation(self):
        return self.rotation
    def getLastRotation(self):
        return self.lastRotation

    def toggleEnableP(self):
        self.enableP = not self.enableP

    def updatePosition(self,movedRotDis):
        rot_cm = movedRotDis[1] * 100 #convert m to cm
        self.lastRotation = self.rotation
        self.rotation = self.rotation + movedRotDis[0]
        if self.rotation > 360:
            self.rotation = self.rotation - 360
        if self.rotation < 0:
            self.rotation = self.rotation + 360

        self.lastLocX = self.locX
        self.lastLocY = self.locY
            
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
    
    def drawVertex(offset,self):
        x = int(self.lastLocX + offset[0])
        y = int(self.lastLocY + offset[1])
        pygame.draw.circle(self.screen,(255,0,0),(x,y), 100 *self.cmPerPix, 1)
        pygame.draw.circle(self.screen,(255,0,0),(x,y), 200 *self.cmPerPix, 1)

        for vertex in self.vertexData:
            self.__drawDot(vertex,self.enableP)
    
    def __drawDot(self,vertex,enableP):
        p = int(255 - (vertex.getP() * 255))
        if enableP:
            pygame.draw.circle(self.screen,(p,p,p),(vertex.getX(),vertex.getY()), 5,0)
        else:
            pygame.draw.circle(self.screen,(125,125,125),(vertex.getX(),vertex.getY()), 5,0)

    #this function adds a new vertex and increases the propability of are vertex that are nearby
    def __addVertex(self,vertex):
        self.vertexData.append(vertex) #add vertex with default probability

        
    #iterates through the vertices tat are in range and finds any that are by themselves
    #if they have nothing in range the propbability is reduced
    def __fuseVertexData(self):
        center = Vertex(self.locX,self.locY)
        for i in range(len(self.vertexData)):
            if self.vertexData[i].distanceTo(center) <= self.rangeLimit:
                #is inrange of robot
                inAgreeRange = False #if any other vertex where within the range
                                           #that stops this vertex being rejected
                for j in range(len(self.vertexData)):
                    #dont test against itself
                    if j != i:
                        distance = self.vertexData[j].distanceTo(self.vertexData[i])
                        if distance < self.agreeRange:
                            #increase P on matched vertex (capped at 1)
                            if self.vertexData[j].getP() < 0.9:
                                self.vertexData[j].setP(self.vertexData[j].getP() + 0.1)
                            else:
                                self.vertexData[j].setP(1)
                            #found a match so dont decrease P
                            inAgreeRange = True
                if inAgreeRange == False:
                    #nothing was in agree range
                    #reduce probabilty of being a good reading (capped to 0.1)
                    if self.vertexData[i].getP() > 0.2:
                        self.vertexData[i].setP(self.vertexData[i].getP() - 0.1)
                    else:
                        self.vertexData[i].setP(0.1)
                

#Class that holds simple positional data and a probability number
class Vertex:
    #x and y are coordintes and should always be integers
    #p in a percentage and defaults to 0.5
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
    #calculates distance between this and other vertex
    def distanceTo(self,vertex):
        return math.sqrt(math.pow(vertex.x - self.x,2)+math.pow(vertex.y - self.y,2))

class PathPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
