import numpy as np
import random
import itertools
import scipy.misc
import matplotlib.pyplot as plt


class gameOb():
    def __init__(self,coordinates,size,intensity,channel,reward,name):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.size = size
        self.intensity = intensity
        self.channel = channel
        self.reward = reward
        self.name = name
        
class salesEnv():
    def __init__(self,partial,size,coor):
        self.sizeX = size
        self.sizeY = size
        self.actions = 4
        self.objects = []
        self.partial = partial
        #self.C = coordinates
        for i in range(0, len(coor)):
            for j in range(0, len(coor)):
                if (2 == coor[i][j]):
                    Salesman = gameOb([i, j],1,1,2,None,'Salesman')
                    self.objects.append(Salesman)

                if (1 == coor[i][j]):
                    bug = gameOb([i, j],1,1,1,1,'Good_Response')
                    self.objects.append(bug)

                if (-1 == coor[i][j]):
                    hole = gameOb([i, j],1,1,0,-1,'Bad_Response')
                    self.objects.append(hole)

                continue
            
        a = self.renderEnv()
        #a = self.reset()
        plt.imshow(a,interpolation="nearest")
        
        
    def reset(self):
        self.objects = []
        Salesman = gameOb(self.newPosition(),1,1,2,None,'Salesman')
        self.objects.append(Salesman)
        bug = gameOb(self.newPosition(),1,1,1,1,'Good_Response')
        self.objects.append(bug)
        hole = gameOb(self.newPosition(),1,1,0,-1,'Bad_Response')
        self.objects.append(hole)
        state = self.renderEnv()
        self.state = state
        return state

    def moveChar(self,direction):
        # 0 - up, 1 - down, 2 - left, 3 - right
        salesman = self.objects[0]
        salesmanX = salesman.x
        salesmanY = salesman.y
        penalize = 0.
        if direction == 0 and salesman.y >= 1:
            salesman.y -= 1
        if direction == 1 and salesman.y <= self.sizeY-2:
            salesman.y += 1
        if direction == 2 and salesman.x >= 1:
            salesman.x -= 1
        if direction == 3 and salesman.x <= self.sizeX-2:
            salesman.x += 1     
        if salesman.x == salesmanX and salesman.y == salesmanY:
            penalize = 0.0
        self.objects[0] = salesman
        return penalize
    
    def newPosition(self):
        iterables = [ range(self.sizeX), range(self.sizeY)]
        points = []
        for t in itertools.product(*iterables):
            points.append(t)
        currentPositions = []
        for objectA in self.objects:
            if (objectA.x,objectA.y) not in currentPositions:
                currentPositions.append((objectA.x,objectA.y))
        for pos in currentPositions:
            points.remove(pos)
        location = np.random.choice(range(len(points)),replace=False)
        return points[location]

    def checkGoal(self):
        others = []
        for obj in self.objects:
            if obj.name == 'Salesman':
                salesman = obj
            else:
                others.append(obj)
        ended = False
        for other in others:
            if salesman.x == other.x and salesman.y == other.y:
                self.objects.remove(other)
                if other.reward == 1:
                    self.objects.append(gameOb(self.newPosition(),1,1,1,1,'Good_Response'))
                else: 
                    self.objects.append(gameOb(self.newPosition(),1,1,0,-1,'Bad_Response'))
                return other.reward,False
        if ended == False:
            return 0.0,False

    def renderEnv(self):
        #a = np.zeros([self.sizeY,self.sizeX,3])
        a = np.ones([self.sizeY+2,self.sizeX+2,3])
        a[1:-1,1:-1,:] = 0
        salesman = None
        for item in self.objects:
            a[item.y+1:item.y+item.size+1,item.x+1:item.x+item.size+1,item.channel] = item.intensity
            if item.name == 'Salesman':
                salesman = item
        if self.partial == True:
            a = a[salesman.y:salesman.y+3,salesman.x:salesman.x+3,:]
        b = scipy.misc.imresize(a[:,:,0],[84,84,1],interp='nearest')
        c = scipy.misc.imresize(a[:,:,1],[84,84,1],interp='nearest')
        d = scipy.misc.imresize(a[:,:,2],[84,84,1],interp='nearest')
        a = np.stack([b,c,d],axis=2)
        return a

    def step(self,action):
        penalty = self.moveChar(action)
        reward,done = self.checkGoal()
        state = self.renderEnv()
        if reward == None:
            print(done)
            print(reward)
            print(penalty)
            return state,(reward+penalty),done
        else:
            return state,(reward+penalty),done
