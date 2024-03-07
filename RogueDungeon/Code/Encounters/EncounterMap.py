import random

from Code.Encounters.Encounters import *


class EncounterMap:
    def __init__(self, startEncounter=None):
        self.setConstants()

        if startEncounter is None:
            startEncounter = self.generateFirstMap()
        self.startEncounter = startEncounter
        self.currentEncounter = startEncounter

        self.path = [startEncounter]

    def setConstants(self):
        self.startPosition = (159, 29)
        self.dx, self.dy = 32, 16

    def setCurrentEncounter(self, encounter):
        self.currentEncounter = encounter
        self.path.append(encounter)

    def generateFirstMap(self):
        nEncounters = 7
        x, y = self.startPosition
        start = Start()
        startNode = EncounterNode(start, x, y)
        y += self.dy
        prev, cur = [startNode], []

        for i in range(nEncounters):
            width = len(prev)
            if width >= min(4, nEncounters-i+2):
                converge = True
            elif width <= 2:
                converge = False
            else:
                converge = random.randint(0, 1) == 0

            cur = self.generateEncounterLine(prev, converge, x, y, i+1)
            y += self.dy
            self.generateEncounterConnections(cur, prev)

            prev = cur

        boss = BattleEncounter("Boss", lvl=100)
        endNode = EncounterNode(boss, x=x, y=y)
        for e in cur:
            e.addEncounterPath(endNode)

        return startNode

    def generateEncounterLine(self, previousLine, converge, x, y, lvl):
        n = len(previousLine)
        if converge:
            n -= 1
        else:
            n += 1
        x -= (n//2)*self.dx - (self.dx//2)*((n+1) % 2)

        nextLine = []
        for i in range(n):
            if random.randint(0, 4) == 0:
                encounter = TreasureEncounter(lvl=lvl)
            else:
                encounter = BattleEncounter(lvl=lvl + random.randint(0, 3))

            encounterNode = EncounterNode(encounter, x=x+i*self.dx, y=y)
            nextLine.append(encounterNode)
        return nextLine

    def generateEncounterConnections(self, currentLine, previousLine):
        converge = len(currentLine) < len(previousLine)

        # force connections and currentLine is 1 smaller than previous
        if converge:
            previousLine[0].addEncounterPath(currentLine[0])
            previousLine[-1].addEncounterPath(currentLine[-1])
            previousLine = previousLine[1:-1]

        for i in range(len(previousLine)):
            connected = False
            if len(currentLine[i].getEncounterBackPaths()) == 0 or random.randint(0, 1) == 0:
                previousLine[i].addEncounterPath(currentLine[i])
                connected = True
            if random.randint(0, 1) == 0 or not connected:
                previousLine[i].addEncounterPath(currentLine[i+1])

        if len(currentLine[-1].getEncounterBackPaths()) == 0:
            previousLine[-1].addEncounterPath(currentLine[-1])

    def show(self):
        print('#'*5, "ENCOUNTER MAP", '#'*5)
        reachable = set(self.currentEncounter.iterateEncounters())

        for encounters in self.startEncounter.iterateEncountersPerDepth()[::-1]:
            line = ""
            for encounter in encounters:
                line += encounter.getName()
                if encounter in reachable:
                    line += " GO"
                elif encounter is self.currentEncounter:
                    line += "<---"
                line += "   "
            print(line)

        print('#' * 5, '#'*len("ENCOUNTER MAP"), '#' * 5)
