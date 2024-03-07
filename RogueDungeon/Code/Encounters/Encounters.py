from random import choice

from Code.Encounters.Battles import Battle
from Code.Encounters.EncounterNode import EncounterNode
from Code.Encounters.Rewards import Reward
from Code.Entities.Enemies import *


class Encounter:
    def __init__(self, name, battle=None, reward=None):
        self.name = name
        self.battle = battle
        self.reward = reward

        # encounter state
        self.battleCompleted = self.battle is None
        self.rewardReceived = self.reward is None
        self.completed = self.rewardReceived and self.battleCompleted

    def complete(self):
        self.completed = True

    def completeBattle(self):
        self.battleCompleted = True
        self.isComplete()

    def receiveReward(self):
        self.rewardReceived = True
        self.isComplete()
        return self.reward

    def isComplete(self):
        self.completed = self.rewardReceived and self.battleCompleted
        return self.completed


class Start(Encounter):
    def __init__(self, name="Start"):
        super().__init__(name)


class BattleEncounter(Encounter):
    def __init__(self, name="Battle", lvl=0):
        battle = Battle(lvl)
        name += " lvl " + str(lvl)
        reward = Reward(lvl)
        super().__init__(name, battle=battle, reward=reward)


class TreasureEncounter(Encounter):
    def __init__(self, name="Treasure", lvl=0):
        reward = Reward(lvl)
        name += " lvl " + str(lvl)
        super().__init__(name, reward=reward)
