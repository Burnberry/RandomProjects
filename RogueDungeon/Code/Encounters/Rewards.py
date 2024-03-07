import random
from random import choice

from Code.Logic.Runes import *


class Reward:
    def __init__(self, lvl, rewards=None, generationArgs=None):
        if rewards is None:
            rewards = self.generateReward(lvl, generationArgs)
        self.rewards = rewards

    def generateReward(self, lvl, generationArgs):
        if lvl < random.randint(0, 2):
            return self.getLowReward()
        if lvl < random.randint(1, 4):
            return self.getMediumReward()
        if lvl < random.randint(3, 6):
            return self.getGreatReward()
        return self.getGreaterReward()

    def getLowReward(self):
        return choice([
            [Spike, MinorCorrosion],
            [Push, MinorCorrosion],
            [Spike, Corrosion]
            ])

    def getMediumReward(self):
        return choice([
            [SpikeBlast, Corrosion],
            [SpikeBlast, Corrosion, Push],
            [SpikeBlast, CorrosiveSpray]
            ])

    def getGreatReward(self):
        return choice([
            [BoulderBash, Push],
            [SpikeBlast, CorrosiveSpray, Corrosion],
            [CorrosiveSpray, BoulderBash]
            ])

    def getGreaterReward(self):
        return choice([
            [StoneHail, BoulderBash, SpikeBlast, CorrosiveSpray],
            [StoneHail, Push, SpikeBlast, Corrosion]
            ])
