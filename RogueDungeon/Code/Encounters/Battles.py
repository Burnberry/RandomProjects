from random import choice

from Code.Entities.Enemies import *


class Battle:
    def __init__(self, lvl, enemies=None, generationArgs=None):
        if enemies is None:
            enemies = self.generateEnemies(lvl, generationArgs)
        self.enemies = enemies

    def generateEnemies(self, lvl, generationArgs):
        if generationArgs is None:
            generationArgs = self._getDefaultGenerationArgs()

        if lvl > 20:
            return [AlbinoBat, Snail, Toadstool]

        if lvl > random.randint(6, 10):
            return self.getDeadlyEnemies()
        if lvl > random.randint(4, 7):
            return self.getHardEnemies()
        if lvl > random.randint(2, 5):
            return self.getMediumEnemies()
        if lvl > random.randint(1, 3):
            return self.getEasyEnemies()
        return self.getSuperEasyEnemies()

    def _getDefaultGenerationArgs(self):
        return {
            'n': 4,
            'lvl': 3
        }

    def getSuperEasyEnemies(self):
        return choice([
            [Bat, Spitter],
            [BlobSmall, Spitter]
            ])

    def getEasyEnemies(self):
        return choice([
            [Spider, Spitter, Bat],
            [Spider, Spider, Spider],
            [Spitter, Spitter, Spitter],
            [Bat, Bat, Spitter],
            [Bat, AlbinoBat]
            ])

    def getMediumEnemies(self):
        return choice([
            [Spider, Spitter, Bat, Spitter],
            [Spider, Spider, Spider, Shroomite],
            [Toadstool],
            [BlobSmall, BlobSmall, BlobSmall, Snail],
            [Bat, AlbinoBat, Spitter, Spitter],
            [RotBlobSmall, HobBlobSmall]
            ])

    def getHardEnemies(self):
        return choice([
            [Spitter, Spitter, Snail, Snail],
            [Shroomite, Toadstool, Shroomite],
            [Shroomite, AlbinoBat, Mudslinger, Mudslinger],
            [RotBlobSmall, Shroomite, Mudslinger, Mudslinger],
            [Bat, AlbinoBat, Spitter, Spitter],
            [RotBlobSmall, HobBlobSmall, BlobSmall, BlobSmall]
            ])

    def getDeadlyEnemies(self):
        return choice([
            [HobBlobSmall, Snail, Toadstool],
            [HobBlobSmall, RotBlobSmall, HobBlobSmall, RotBlobSmall],
            [HobBlobSmall, AlbinoBat, Mudslinger, AlbinoBat],
            [RotBlobSmall, Toadstool, RotBlobSmall]
            ])
