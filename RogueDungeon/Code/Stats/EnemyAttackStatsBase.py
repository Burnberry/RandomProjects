from Code.Stats.AttackStatsBase import AttackStatsBase


class EnemyAttackStatsBase(AttackStatsBase):
    """
    Data storage class for enemy attack stats
    Allows for easy default values for different attacks, so changing values can be delayed after testing
    """
    tierPrimary = 10
    tierSecondary = 6
    tierFail = 3
    tierCriticalFail = 0

    def __init__(self, name, description="", tier=tierPrimary, turns=1, positions=None, alternativeAttacks=None, **attackArgs):
        super().__init__(name, description, **attackArgs)

        if positions is None:
            positions = [0, 1, 2, 3]
        self.positionToAttack = {}
        if alternativeAttacks is None:
            alternativeAttacks = {}
        for pos in alternativeAttacks:
            self.positionToAttack[pos] = alternativeAttacks[pos]()
        for pos in positions:
            self.positionToAttack[pos] = self

        self.turns = turns
        self.tier = tier
        self.positionText = self.getPositionText()

    def getDisplayText(self, turns=0):
        if self.turns - turns == 0:
            turnText = ""
        else:
            turnText = " in " + str(self.turns - turns)
        return self.name + turnText

    def getPositionText(self):
        text = ""
        for pos in range(4):
            tier = self.getAttackStats(pos).tier
            if tier == self.tierSecondary:
                c = "o "
            elif tier == self.tierFail:
                c = "_ "
            elif tier == self.tierCriticalFail:
                c = "X "
            else:
                c = "O "

            text += c
        return text[:-1]

    def getAttackStats(self, position):
        if position in self.positionToAttack:
            return self.positionToAttack[position]
        else:
            print(position, "out of bounds for attack card", self.name)
            return self

    def canActivate(self):
        return self.turns <= 1
