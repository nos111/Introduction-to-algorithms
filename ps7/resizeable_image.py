import imagematrix
import sys
energyDict = {}
class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        energyDict = {}
        bestSeamList = []
        neighborsList = []
        temp = ()
        dp = []
        for j in range(0, self.width - 1):
            bestSeamList = []
            dp.append([])
            dp[j].append(0)
            bestSeamList.append((j,0))
            bestSeamList.append((j,1))
            for i in range(1, self.height - 1):
                #print("I is ",i)
                #print("currently looking at ", bestSeamList[i])
                neighborsList = self.getNeighbors(bestSeamList[i][0], bestSeamList[i][1])
                tempEnerg = self.getEnergy(bestSeamList[i][0], bestSeamList[i][1])
                temp = self.findMinEnergyNeighbors(neighborsList, tempEnerg)
                dp[j][0] = dp[j][0] + tempEnerg
                print("the neighbors are ", temp)
                bestSeamList.append(temp)

            dp[j].append(bestSeamList)
        lowestValue = sys.maxint
        index = 0
        for x in range(0, len(dp)):
            temp = dp[x][0]
            if lowestValue > temp:
                lowestValue = temp
                index = x

        return dp[index][1]

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def findLowestEnergyTop(self):
        lowestEnergy = self.energy(1,1)
        for x in range(1, self.width - 1):
            if(self.getEnergy(x,1) < lowestEnergy):
                lowestEnergy = self.getEnergy(x,1)
        return lowestEnergy
    def getEnergy(self, x, y):
        try:
            return energyDict[(x,y)]
        except KeyError:
            energyDict[(x,y)] = self.energy(x,y)
            return energyDict[(x,y)]
    def getNeighbors(self, x, y):
        if x == self.width - 1:
            return [(x,y+1), (x-1, y+1)]
        elif x == 0:
            return [(x, y+1), (x+1, y+1)]
        #print("the start pixel coordinates is ", x, " ", y)
        return [(x-1,y+1), (x, y+1), (x+1, y+1)]

    def findMinEnergyNeighbors(self, neighborList, currentPixEnergy):
        print("the neighbors are  ", neighborList)
        lowestEnergy = currentPixEnergy + self.getEnergy(neighborList[0][0], neighborList[0][1])
        cordinate = (neighborList[0][0], neighborList[0][1])
        for cor in neighborList:
            
            energy = self.getEnergy(cor[0], cor[1])
            print("energy is ",energy + currentPixEnergy)
            if(energy + currentPixEnergy > lowestEnergy):
                lowestEnergy = energy + currentPixEnergy
                cordinate = cor
        print("\n")
        return cordinate




    

