from Code.Stats.RuneStatsBase import RuneStatsBase


class RuneStatsSpike(RuneStatsBase):
    def __init__(self):
        name = "Spike"
        description = "Piercing projectile"
        super().__init__(name, description=description, pierceDamage=2)


class RuneStatsSpikeBlast(RuneStatsBase):
    def __init__(self):
        name = "Spike Blast"
        description = "Volley of piercing projectiles"
        super().__init__(name, description=description, pierceDamage=2, isAreaAttack=True)


class RuneStatsMinorCorrosion(RuneStatsBase):
    def __init__(self):
        name = "Minor Corrosion"
        description = "Corrodes one enemy"
        super().__init__(name, description=description, corrosion=1)


class RuneStatsCorrosion(RuneStatsBase):
    def __init__(self):
        name = "Corrosion"
        description = "Corrodes one enemy"
        super().__init__(name, description=description, corrosion=2)


class RuneStatsCorrosiveSpray(RuneStatsBase):
    def __init__(self):
        name = "Corrosive Spray"
        description = "Corrodes all enemies"
        super().__init__(name, description=description, corrosion=1, isAreaAttack=True)


class RuneStatsPush(RuneStatsBase):
    def __init__(self):
        description = "Can move an enemy"
        super().__init__("Push", description=description, push=2, force=2)


class RuneStatsBoulderBash(RuneStatsBase):
    def __init__(self):
        description = "Summons and hurls a boulder. Can stun and push back an enemy."
        super().__init__("Boulder Bash", description=description, positions=[0, 1], damage=6, push=1, force=1, canStun=True)


class RuneStatsStoneHail(RuneStatsBase):
    def __init__(self):
        description = "Summons a boulder high in the sky and explodes it, raining fragments aground"
        super().__init__("Stone Hail", description=description, damage=4, isAreaAttack=True)






# Legacy attacks
class RuneStatsBash(RuneStatsBase):
    def __init__(self):
        description = "Can move an enemy"
        super().__init__("Push", description=description, push=2, force=1)


class RuneStatsBaseBasicAttack(RuneStatsBase):
    def __init__(self):
        description = ""
        super().__init__("Basic Attack", description=description, damage=3)


class RuneStatsBaseSmash(RuneStatsBase):
    def __init__(self):
        description = "Close range strike which can stun. (If stuns were implemented)"
        super().__init__("Smash", description=description, positions=[0, 1], damage=5, force=1)


class RuneStatsBasePoisonBlast(RuneStatsBase):
    def __init__(self):
        description = "Poisons enemy"
        super().__init__("Poison Blast", description=description, positions=[1, 2], damage=2, poison=2)


class RuneStatsBasePush(RuneStatsBase):
    def __init__(self):
        description = "Can move an enemy"
        super().__init__("Push", description=description, push=2)
