class AttackStatsBase:
    def __init__(self, name, description="", movement=0, push=0, force=0, canStun=False, damage=0, pierceDamage=0, poison=0, corrosion=0, phlogiston=0, buffs=None, healthDrainLevel=0, isAreaAttack=False, isAreaBuff=False):
        self.name = name
        self.description = description
        self.positionText = "- - - -"

        self.movement = movement
        self.push, self.force = push, force
        self.canStun = canStun

        self.damage = damage
        self.pierceDamage = pierceDamage
        self.poison = poison
        self.corrosion = corrosion
        self.phlogiston = phlogiston

        self.buffs = buffs

        self.healthDrainLevel = healthDrainLevel
        self.isAreaAttack = isAreaAttack
        self.isAreaBuff = isAreaBuff

    def getHoverText(self):
        text = self.name + "\n"
        text += self.getPositionText() + "\n"
        if len(self.description):
            text += self.description + "\n"

        if self.movement > 0:
            text += str(self.movement) + " =>\n"
        if self.movement < 0:
            text += str(self.movement) + " <=\n"
        if self.push > 0:
            text += str(self.push) + " =>\n"
        if self.push < 0:
            text += str(self.push) + " <=\n"
        if self.push < 0:
            text += str(self.push) + " <=\n"

        if self.damage > 0:
            text += str(self.damage) + " damage\n"
        if self.poison > 0:
            text += str(self.poison) + " poison\n"
        if self.phlogiston > 0:
            text += str(self.phlogiston) + " phlogiston\n"

        return text[:-1]

    def getPositionText(self):
        return self.positionText
