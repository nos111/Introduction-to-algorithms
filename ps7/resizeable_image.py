import imagematrix
energyDict = {}
class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        bestSeamList = []
        lowest = self.findLowestEnergyTop()
        bestSeamList.append((lowest,0))
        bestSeamList.append((lowest,1))
        neighborsList = []
        temp = ()
        for i in range(1, self.height - 1):
            print("I is ",i)
            print("currently looking at ", bestSeamList[i])
            neighborsList = self.getNeighbors(bestSeamList[i][0], bestSeamList[i][1])
            tempEnerg = self.getEnergy(bestSeamList[i][0], bestSeamList[i][1])
            temp = self.findMinEnergyNeighbors(neighborsList, tempEnerg)
            bestSeamList.append(temp)
        return bestSeamList

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
        print("the start pixel coordinates is ", x, " ", y)
        return [(x-1,y+1), (x, y+1), (x+1, y+1)]

    def findMinEnergyNeighbors(self, neighborList, currentPixEnergy):
        lowestEnergy = currentPixEnergy + self.getEnergy(neighborList[0][0], neighborList[0][1])
        cordinate = (neighborList[0][0], neighborList[0][1])
        for cor in neighborList:
            energy = self.getEnergy(cor[0], cor[1])
            if(energy + currentPixEnergy < lowestEnergy):
                lowestEnergy = energy + currentPixEnergy
                cordinate = cor
        return cordinate




    

