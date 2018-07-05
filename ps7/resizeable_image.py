import imagematrix
import sys
energyDict = {}
track = {}
dp = {}
class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        global energyDict
        energyDict = {}
        global dp 
        dp = {}
        global track
        track = {}
        startCord = ()
        bestSeam = []
        self.fillFirstRow()
        for j in range(1, self.height):
            for i in range(0, self.width):
                self.updateNeighborEnergy(i,j)
        startCord = self.findLowestValue()
        bestSeam = self.buildTrack(startCord)
        return bestSeam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def fillFirstRow(self):
        for x in range(0, self.width ):
            dp[x,0] = self.getEnergy(x,0)
        
    def getEnergy(self, x, y):
        try:
            return energyDict[(x,y)]
        except KeyError:
            energyDict[(x,y)] = self.energy(x,y)
            return energyDict[(x,y)]

    def getNeighbors(self, x, y):
        if x == self.width - 1:
            return [(x,y-1), (x-1, y-1)]
        elif x == 0:
            return [(x, y-1), (x+1, y-1)]
        return [(x-1,y-1), (x, y-1), (x+1, y-1)]

    def updateNeighborEnergy(self, x, y):
        neighborsList = self.getNeighbors(x, y)
        currentPixEnerg = self.getEnergy(x,y)
        #print "energy of pix ",x,y, currentPixEnerg
        dp[x,y] = currentPixEnerg + dp[x,y - 1]
        track[x,y] = 0
        for cor in neighborsList:
            energy = dp[cor[0], cor[1]]
            if(energy + currentPixEnerg < dp[x,y]):
                dp[x,y] = energy + currentPixEnerg
                track[x,y] = x - cor[0]
        #print "updated ", x , y, "with track ", track[x,y]

    def findLowestValue(self):
        lowest = dp[0, self.height - 1]
        coordinates = (0, self.height - 1)
        for x in range(0, self.width - 1):
            if(dp[x,self.height - 1] < lowest):
                lowest = dp[x,self.height - 1]
                coordinates = (x,self.height - 1)
        print "lowest value ", lowest
        return coordinates

    def buildTrack(self, startCoord):
        bestTrack = []
        #print "start coordinates ", startCoord
        bestTrack.append(startCoord)
        #print "adding ", (bestTrack[0][0] , bestTrack[0][1] ), self.getEnergy(bestTrack[0][0], bestTrack[0][1])
        for i in range(0, self.height - 1):
            x = track[bestTrack[i][0], bestTrack[i][1]]
            #print "adding ", (bestTrack[i][0] - x, bestTrack[i][1] - 1), self.getEnergy(bestTrack[i][0] - x, bestTrack[i][1] - 1)
            #print "x is ", x
            bestTrack.append((bestTrack[i][0] - x, bestTrack[i][1] - 1))
        return bestTrack



    

