from random import randint


class EncounterNode:
    def __init__(self, encounter, x, y, isDestination=False):
        self.setConstants()

        self.encounter = encounter
        self.name = self.encounter.name

        # encounter Node logic
        self.x0, self.y0 = x, y
        self.x, self.y = self.getRandomPosition()

        self.isDestination = isDestination

        self.encounterPaths = []
        self.encounterBackPaths = []
        self.isCompleted = False

    def getPosition(self):
        return self.x, self.y

    def getNodePosition(self):
        """
        Gives the original graph position without random movement
        :return: x, y
        """
        return self.x0, self.y0

    def getRandomPosition(self):
        x, y = self.getNodePosition()
        x += randint(-self.dxRandom, self.dxRandom)
        y += randint(-self.dyRandom, self.dyRandom)
        return x, y

    def getName(self):
        return self.name

    def getFullName(self):
        return self.getName() + " (" + str(self.x) + ", " + str(self.y) + ")"

    def getEncounterPaths(self):
        return self.encounterPaths

    def getEncounterBackPaths(self):
        return self.encounterBackPaths

    def getStartEncounter(self):
        cur = self
        while len(cur.getEncounterBackPaths()) > 0:
            cur = cur.getEncounterBackPaths()[0]

        return cur

    def setConstants(self):
        self.dxRandom, self.dyRandom = 4, 4

    def setReachable(self, reachable):
        self.reachable = reachable

    def addEncounterPath(self, encounter):
        self.encounterPaths.append(encounter)
        encounter.addEncounterBackPath(self)

    def addEncounterBackPath(self, encounter):
        self.encounterBackPaths.append(encounter)

    def isCompleted(self):
        return self.isCompleted

    def complete(self):
        self.isCompleted = True

    def iterateEncounters(self, includeSelf=False, depth=-1):
        """
        gives list of all encounters reachable from this encounter
        :param includeSelf: encounter
        :param depth: max number of jumps
        :return: list->encounter
        """

        encounters = []
        if includeSelf:
            encounters.append(self)

        seen = {self}

        nextEncounters = {self}
        while len(nextEncounters) > 0 and depth != 0:
            newNextEncounters = set()
            for encounter in nextEncounters:
                for e in encounter.getEncounterPaths():
                    if e not in seen:
                        seen.add(e)
                        newNextEncounters.add(e)
                        encounters.append(e)
            nextEncounters = newNextEncounters
            depth -= 1

        return encounters

    def iterateEncountersPerDepth(self):
        """
        gives lists of encounters reachable from this encounter in order of required jumps to reach
        first list is always itself
        :return: list->list->encounter
        """
        encountersPerDepth = []
        seen = {self}

        nextEncounters = {self}
        while len(nextEncounters) > 0:
            encountersPerDepth.append(list(nextEncounters))
            newNextEncounters = set()
            for encounter in nextEncounters:
                for e in encounter.getEncounterPaths():
                    if e not in seen:
                        seen.add(e)
                        newNextEncounters.add(e)
            nextEncounters = newNextEncounters

        return encountersPerDepth
