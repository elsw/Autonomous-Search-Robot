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

        
        self.rangeLimit = 200 #this is the max range that readings are tacken as true
        self.fusionRange = 0 #range for vertexes to affect each others probability (in cm)
        self.rejectionRange = 300 #anything above this will lose propability if not back up by other readings
    
                
    def addRangeData(self,rangeData):
        for r in rangeData:
            angle = r.angle - 90 + self.rotation
            x = self.locX + r.distance *self.cmPerPix* math.cos(math.radians(angle))
            y = self.locY + r.distance *self.cmPerPix* math.sin(math.radians(angle))
            self.__addVertex(Vertex(int(x),int(y)))
        self.__fuseVertexData()
    

    def getPosition(self):
        return (self.locX,self.locY)
    def getRotation(self):
        return self.rotation

    def updatePosition(self,movedRotDis):
        rot_cm = movedRotDis[1] * 100 #convert m to cm
        self.rotation = self.rotation + movedRotDis[0]
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
            self.__drawDot(vertex)
    
    def __drawDot(self,vertex):
        p = int(255 - (vertex.getP() * 255))
        pygame.draw.circle(self.screen,(p,p,p),(vertex.getX(),vertex.getY()), 5,0)

    #this function adds a new vertex and increases the propability of are vertex that are nearby
    def __addVertex(self,vertex):
        self.vertexData.append(vertex) #add vertex with default probability

        
    #iterates through the vertices tat are in range and finds any that are by themselves
    #if they have nothing in range the propbability is reduced
    def __fuseVertexData(self):
        center = Vertex(self.locX,self.locY)
        for i in range(len(self.vertexData)):
            if i < len(self.vertexData) and self.vertexData[i].distanceTo(center) <= self.rangeLimit:
                #is inrange of robot
                inRejectRange = False #if any other vertex where within the range
                                           #that stops this vertex being rejected
                for j in range(len(self.vertexData)):
                    #dont test against itself
                    if j != i:
                        distance = self.vertexData[j].distanceTo(self.vertexData[i])
                        if distance < self.rejectionRange:
                            #mark that this vertex wont be reduced in probability
                            inRejectRange = True
                        if distance < self.fusionRange:
                            #fuse vertices
                            #interpolate new vertex depending on propability difference
                            #pInterpolate is between 0 and 1, 0.5 being both the same P
                            pInt = (0.5 + (self.vertexData[i].getP() - self.vertexData[j].getP())/2)
                            vXi = self.vertexData[i].getX()
                            vYi = self.vertexData[i].getY()
                            vXj = self.vertexData[i].getX()
                            vYj = self.vertexData[i].getY()
                            newX = vXi + ((vXj - vXi)* pInt)
                            newY = vYi + ((vYj - vYi)* pInt)
                            newP = 0.5
                            if self.vertexData[i].getP() > self.vertexData[j].getP():
                                newP = self.vertexData[i].getP()
                            else:
                                newP = self.vertexData[j].getP()
                            if newP < 0.8:
                                newP = newP + 0.2
                            else:
                                newP = 1
                            #remove both old vertices
                            self.vertexData.pop(i)
                            self.vertexData.pop(j)
                            #add new vertex
                            self.vertexData.append(Vertex(newX,newY,newP))
                            #print "fuse"
                            break
                if inRejectRange == False:
                    #print "none in range"
                    #nothing was in reject range
                    #reduce probabilty of being a good reading
                    if self.vertexData[i].getP() > 2:
                        self.vertexData[i].setP(self.vertexData[i].getP() - 0.2)
                    else:
                        self.vertexData[i].setP(0)
                

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
        
