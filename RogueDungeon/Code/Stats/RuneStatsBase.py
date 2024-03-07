from Code.Stats.AttackStatsBase import AttackStatsBase


class RuneStatsBase(AttackStatsBase):
    """
    Data storage class for card stats
    Allows for easy default values for different cards, so changing values can be delayed after testing
    """

    def __init__(self, name, description="", tier=1, positions=None, alternative_attacks=None, **attackArgs):
        super().__init__(name, description, **attackArgs)

        if positions is None:
            positions = [0, 1, 2, 3]
        self.positionToRuneAttack = {}
        if alternative_attacks is None:
            alternative_attacks = {}
        for pos in alternative_attacks:
            self.positionToRuneAttack[pos] = alternative_attacks[pos]()
        for pos in positions:
            self.positionToRuneAttack[pos] = self

        self.tier = tier
        self.positionText = self.getPositionText()

    def getPositionText(self):
        text = ""
        for pos in range(4):
            if pos not in self.positionToRuneAttack:
                text += "_ "
                continue
            rune = self.positionToRuneAttack[pos]
            if rune.tier == 1:
                text += "O "
            elif rune.tier == 0:
                text += "o "
            else:
                print("undefined rune tier")
        return text[:-1]

    def isValidUse(self, position, enemy):
        return self.isValidPosition(position) and self.isValidEnemy(position, enemy)

    def isValidPosition(self, position):
        rune = self.positionToRuneAttack.get(position, None)
        return rune is not None

    def isValidEnemy(self, position, enemy):
        rune = self.positionToRuneAttack.get(position, None)
        # todo
        return True
