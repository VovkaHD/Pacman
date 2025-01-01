import os
from random import randint


class GameEngine(object):

    def __init__(self):

        self.levelPelletRemaining = 0
        self.levelObjects = [[levelObject("empty") for j in range(32)] for i in range(28)]
        self.movingObjectPacman = movingObject("Pacman")
        self.movingObjectGhosts = [movingObject("Ghost") for n in range(4)]

        self.levelObjectNamesBlocker = ["wall", "cage"]
        self.levelObjectNamesPassable = ["empty", "pellet", "powerup"]


    def levelGenerate(self, level):
        pathCurrentDir = os.path.dirname(__file__)
        pathRelDir = "../resource/level{}.txt".format(level)
        pathAbsDir = os.path.join(pathCurrentDir, pathRelDir)

        levelFile = open(pathAbsDir, encoding="utf-8")
        levelLineNo = 0

        for levelLine in levelFile.readlines():

            levelLineSplit = list(levelLine)

            for i in range(28):

                if levelLineSplit[i] == "_":
                    self.levelObjects[i][levelLineNo].name = "empty"
                elif levelLineSplit[i] == "#":
                    self.levelObjects[i][levelLineNo].name = "wall"
                elif levelLineSplit[i] == "$":
                    self.levelObjects[i][levelLineNo].name = "cage"


                elif levelLineSplit[i] == ".":
                    self.levelObjects[i][levelLineNo].name = "pellet"

                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "*":
                    self.levelObjects[i][levelLineNo].name = "powerup"

                    if self.levelObjects[i][levelLineNo].isDestroyed == False:
                        self.levelPelletRemaining += 1
                    else:
                        pass


                elif levelLineSplit[i] == "@":
                    self.levelObjects[i][levelLineNo].name = "empty"

                    self.movingObjectPacman.coordinateRel[0] = i
                    self.movingObjectPacman.coordinateRel[1] = levelLineNo
                    self.movingObjectPacman.coordinateAbs[0] = i * 4
                    self.movingObjectPacman.coordinateAbs[1] = levelLineNo * 4


                elif levelLineSplit[i] == "&":
                    self.levelObjects[i][levelLineNo].name = "empty"

                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].isCaged = False
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break


                elif levelLineSplit[i] == "%":
                    self.levelObjects[i][levelLineNo].name = "empty"

                    for n in range(4):
                        if self.movingObjectGhosts[n].isActive == False:
                            self.movingObjectGhosts[n].isActive = True
                            self.movingObjectGhosts[n].coordinateRel[0] = i
                            self.movingObjectGhosts[n].coordinateRel[1] = levelLineNo
                            self.movingObjectGhosts[n].coordinateAbs[0] = i * 4
                            self.movingObjectGhosts[n].coordinateAbs[1] = levelLineNo * 4
                            break


            levelLineNo += 1
        levelFile.close()


    def encounterFixed(self, x, y):
        if self.levelObjects[x][y].name == "empty":
            result = "empty"

        elif self.levelObjects[x][y].name == "pellet":
            result = "pellet"

        elif self.levelObjects[x][y].name == "powerup":
            result = "powerup"
        
        return result

    
    def encounterMoving(self, x, y):

        result = "alive"

        for i in range(4):
            m = self.movingObjectGhosts[i].coordinateAbs[0]
            n = self.movingObjectGhosts[i].coordinateAbs[1]

            if self.movingObjectGhosts[i].isActive == True and self.movingObjectGhosts[i].isCaged == False:
                if (m-3 < x < m+3) and (n-3 < y < n+3):
                    result = "dead"
                else:
                    pass
            else:
                pass
        
        return result



    def loopFunction(self):
        self.movingObjectPacman.MoveNext(self)
        self.movingObjectPacman.MoveCurrent(self)

        for i in range(4):
            if self.movingObjectGhosts[i].isActive == True:
                self.movingObjectGhosts[i].dirNext = self.movingObjectGhosts[i].MoveNextGhost(self, self.movingObjectGhosts[i].dirCurrent)
                self.movingObjectGhosts[i].MoveNext(self)
                self.movingObjectGhosts[i].MoveCurrent(self)
            
            else:
                pass






class levelObject(object):

    def __init__(self, name):
        self.reset(name)

    def reset(self, name):
        self.name = name
        self.isDestroyed = False



class movingObject(object):

    def __init__(self, name):
        self.reset(name)


    def reset(self, name):
        self.name = name
        self.isActive = False
        self.isCaged = True
        self.dirCurrent = "Left"
        self.dirNext = "Left"
        self.dirOpposite = "Right"
        self.dirEdgePassed = False
        self.coordinateRel = [0, 0]
        self.coordinateAbs = [0, 0]


    def MoveNextGhost(self, GameEngine, dirCur):

        if self.isCaged == True:
            pass

        elif self.coordinateAbs[0] % 4 != 0:
            pass

        elif self.coordinateAbs[1] % 4 != 0:
            pass
        
        else:
            dirIndex = ['Left', 'Right', 'Up', 'Down']
            dirAvailable = []
            dirDOF = 0

            if dirCur == 'Left':
                self.dirOpposite = 'Right'
            elif dirCur == 'Right':
                self.dirOpposite = 'Left'
            elif dirCur == 'Up':
                self.dirOpposite = 'Down'
            elif dirCur == 'Down':
                self.dirOpposite = 'Up'
            else:
                pass

            try:
                for i in range(4):

                    if i == 0:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]]
                    elif i == 1:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]]
                    elif i == 2:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1]
                    elif i == 3:
                        nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1]

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        dirDOF += 1
                        dirAvailable.append(dirIndex[i])
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass

            except IndexError:
                dirDOF = 2
                dirAvailable.append(dirCur)
            

            try:
                if dirDOF == 1:
                    return dirAvailable[0]
                
                elif dirDOF == 2:
                    if dirCur in dirAvailable:
                        return dirCur
                    elif dirCur == 'Stop':
                        return dirAvailable[0]
                    else:
                        dirAvailable.remove(self.dirOpposite)
                        return dirAvailable[0]


                elif dirDOF == 3 or dirDOF == 4:
                    if dirCur == 'Stop':
                        randNo = randint(0, dirDOF-1)
                        return dirAvailable[randNo]
                    else:
                        dirAvailable.remove(self.dirOpposite)
                        randNo = randint(0, dirDOF-2)
                        return dirAvailable[randNo]
            

            except ValueError:
                pass



    def MoveNext(self, GameEngine):

        if self.dirNext == self.dirCurrent:
            pass
        
        elif self.coordinateAbs[0] % 4 != 0:
            pass

        elif self.coordinateAbs[1] % 4 != 0:
            pass

        else:
            if self.dirNext == "Left":

                if self.coordinateRel[0] == 0:
                    self.dirCurrent = "Left"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]]

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Left"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass
                

            elif self.dirNext == "Right":

                if self.coordinateRel[0] == 27:
                    self.dirCurrent = "Right"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]]

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Right"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Down":

                if self.coordinateRel[1] == 31:
                    self.dirCurrent = "Down"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1]

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Down"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass


            elif self.dirNext == "Up":

                if self.coordinateRel[1] == 0:
                    self.dirCurrent = "Up"

                else:
                    nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1]

                    if nextObject.name in GameEngine.levelObjectNamesPassable:
                        self.dirCurrent = "Up"
                    elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                        pass

        
    
    def MoveCurrent(self, GameEngine):

        if self.dirCurrent == "Left":

            if self.coordinateAbs[0] == 0:
                self.coordinateAbs[0] = 27*4 + 3
                self.coordinateRel[0] = 28
                self.dirEdgePassed = True
            
            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]-1][self.coordinateRel[1]]
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] -= 1
                    if self.coordinateAbs[0] % 4 == 0:
                        self.coordinateRel[0] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Right":

            if self.coordinateAbs[0] == 27*4:
                self.coordinateAbs[0] = -3
                self.coordinateRel[0] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]+1][self.coordinateRel[1]]
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[0] += 1
                    if self.coordinateAbs[0] % 4 == 0:
                        self.coordinateRel[0] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Down":

            if self.coordinateAbs[1] == 31*4:
                self.coordinateAbs[1] = -3
                self.coordinateRel[1] = -1
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]+1]
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] += 1
                    if self.coordinateAbs[1] % 4 == 0:
                        self.coordinateRel[1] += 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Up":

            if self.coordinateAbs[1] == 0:
                self.coordinateAbs[1] = 31*4 + 3
                self.coordinateRel[1] = 32
                self.dirEdgePassed = True

            else:
                nextObject = GameEngine.levelObjects[self.coordinateRel[0]][self.coordinateRel[1]-1]
                if nextObject.name in GameEngine.levelObjectNamesPassable:
                    self.coordinateAbs[1] -= 1
                    if self.coordinateAbs[1] % 4 == 0:
                        self.coordinateRel[1] -= 1

                elif nextObject.name in GameEngine.levelObjectNamesBlocker:
                    self.dirCurrent = "Stop"


        elif self.dirCurrent == "Stop":
            pass


gameEngine = GameEngine()