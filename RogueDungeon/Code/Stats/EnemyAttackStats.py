from Code.Stats.EnemyAttackStatsBase import EnemyAttackStatsBase


# generic moves
class Stumble(EnemyAttackStatsBase):
    def __init__(self):
        description = "Wastes an action out of balance"
        super().__init__("Stumble", description=description, tier=EnemyAttackStatsBase.tierFail)


class Idle(EnemyAttackStatsBase):
    def __init__(self):
        description = "Sometimes you just need a break. Watch the clouds, smell some flowers, other matters can wait."
        super().__init__("Idle", description=description, turns=1)


_stumbles = {pos: Stumble for pos in range(5)}


# Offensive Attacks
class Lunge(EnemyAttackStatsBase):
    def __init__(self):
        description = "Moves forward to attack"
        super().__init__("Lunge", description=description, turns=2, damage=3, positions=[2, 3], alternativeAttacks=_stumbles, movement=-2)


class VenomousBite(EnemyAttackStatsBase):
    def __init__(self):
        description = "Close range attack"
        super().__init__("Venomous Bite", description=description, turns=3, damage=2, positions=[0, 1], alternativeAttacks=_stumbles, poison=2)


class Slam(EnemyAttackStatsBase):
    def __init__(self):
        description = "Attack using full body."
        super().__init__("Slam", description=description, turns=5, damage=7, positions=[0, 1, 2, 3], alternativeAttacks=_stumbles)


class Spit(EnemyAttackStatsBase):
    def __init__(self):
        description = "Forceful projectile of phlegm."
        super().__init__("Spit", description=description, turns=2, damage=4, positions=[2, 3], alternativeAttacks=_stumbles)


class VenomousHarpoon(EnemyAttackStatsBase):
    def __init__(self):
        description = "Harpoon attack coated in paralyzing venom"
        super().__init__("Venomous Harpoon", description=description, turns=1, pierceDamage=2, poison=3, force=1, canStun=True, positions=[0], alternativeAttacks=_stumbles)


class VampiricBite(EnemyAttackStatsBase):
    def __init__(self):
        description = "A quick bite draining some blood"
        super().__init__("Vampiric Bite", description=description, turns=2, damage=3, healthDrainLevel=1, positions=[0, 1], alternativeAttacks=_stumbles)


class BloodDrain(EnemyAttackStatsBase):
    def __init__(self):
        description = "Feeding on blood invigorates the creature"
        super().__init__("Blood Drain", description=description, turns=2, damage=5, healthDrainLevel=2, positions=[0], alternativeAttacks=_stumbles)


class Swoop(EnemyAttackStatsBase):
    def __init__(self):
        description = "Quickly plunges forward into a target"
        positions = [1, 2, 3]
        super().__init__("Swoop", description=description, turns=2, damage=2, movement=-3, positions=positions, alternativeAttacks=_stumbles)


class Ram(EnemyAttackStatsBase):
    def __init__(self):
        description = "Head forward, rams into a target"
        positions = [0, 1, 2]
        super().__init__("Ram", description=description, turns=2, damage=2, movement=-1, positions=positions, alternativeAttacks=_stumbles)


class Wiggle(EnemyAttackStatsBase):
    def __init__(self):
        description = "Strange bodily movements while making whimsical screeches"
        positions = [0, 1, 2, 3]
        super().__init__("Wiggle", description=description, turns=1, positions=positions, alternativeAttacks=_stumbles)


class Sporulate(EnemyAttackStatsBase):
    def __init__(self):
        description = "Releases spores"
        positions = [0, 1, 2, 3]
        buffs = {"regeneration": 2}
        super().__init__("Sporulate", description=description, turns=1, poison=2, isAreaBuff=True, buffs=buffs, positions=positions, alternativeAttacks=_stumbles)


class MudSling(EnemyAttackStatsBase):
    def __init__(self):
        description = ""
        positions = [2, 3]
        super().__init__("Mud Sling", description=description, turns=3, damage=4, positions=positions, alternativeAttacks=_stumbles)


class Harden(EnemyAttackStatsBase):
    def __init__(self):
        description = "Adds some shield to the creature"
        positions = [0, 1, 2, 3]
        buffs = {"block": 5}
        super().__init__("Harden", description=description, turns=2, buffs=buffs, positions=positions, alternativeAttacks=_stumbles)


class MudCoats(EnemyAttackStatsBase):
    def __init__(self):
        description = "Covers all creatures in a muddy shield"
        positions = [0, 1, 2, 3]
        buffs = {"block": 3}
        super().__init__("Mud Coats", description=description, turns=3, buffs=buffs, positions=positions, isAreaBuff=True, alternativeAttacks=_stumbles)


class Shriek(EnemyAttackStatsBase):
    def __init__(self):
        description = "A piercing screech"
        positions = [1, 2, 3]
        super().__init__("Shriek", description=description, pierceDamage=5, turns=3, positions=positions, alternativeAttacks=_stumbles)


class FoulFlower(EnemyAttackStatsBase):
    def __init__(self):
        description = "Horrific stench causing sickness"
        positions = [0]
        super().__init__("Foul Flower", description=description, poison=7, turns=5, positions=positions, alternativeAttacks=_stumbles)


# Pure movement
class MarchForth(EnemyAttackStatsBase):
    def __init__(self):
        description = ""
        super().__init__("March Forth", description=description, turns=1, movement=-1, alternativeAttacks=_stumbles)


class MarchBack(EnemyAttackStatsBase):
    def __init__(self):
        description = ""
        super().__init__("March Back", description=description, turns=1, movement=1, alternativeAttacks=_stumbles)


class OozleForth(EnemyAttackStatsBase):
    def __init__(self):
        description = "Slowly creeping to you"
        super().__init__("Oozle Forth", description=description, turns=2, movement=-1, alternativeAttacks=_stumbles)


class OozleBack(EnemyAttackStatsBase):
    def __init__(self):
        description = "Slowly creeping away"
        super().__init__("Oozle Back", description=description, turns=2, movement=1, alternativeAttacks=_stumbles)


class LeapForth(EnemyAttackStatsBase):
    def __init__(self):
        description = ""
        super().__init__("Leap Forth", description=description, turns=1, movement=-2, alternativeAttacks=_stumbles)


class LeapBack(EnemyAttackStatsBase):
    def __init__(self):
        description = ""
        super().__init__("Leap Back", description=description, turns=1, movement=2, alternativeAttacks=_stumbles)
