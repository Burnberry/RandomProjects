import Code.Entities.Enemies as Enemies
from Code.Stats.EnemyAttackStats import *
from Code.Stats.EntityStatsBase import EntityStatsBase


class StatsPlayerBase(EntityStatsBase):
    def __init__(self):
        description = "This is you. Don't die."
        super().__init__("Player", description=description, health=100)


class StatsSpiderBase(EntityStatsBase):
    def __init__(self):
        attacks = [Lunge(), VenomousBite()]
        description = "Nimble critter with venomous fangs."
        corpse = Enemies.CorpseSmall
        super().__init__("Spider", description=description, corpse=corpse,  health=5, attacks=attacks)


class StatsSnailBase(EntityStatsBase):
    def __init__(self):
        attacks = [OozleForth, OozleBack, VenomousHarpoon]
        description = "Very slow creature, not a threat from a distance."
        corpse = Enemies.CorpseSmall
        super().__init__("Snail", description=description, corpse=corpse,  health=7, shield=19, defaultForceBlock=5, attacks=attacks)


class StatsBlobSmallBase(EntityStatsBase):
    def __init__(self):
        attacks = [Slam()]
        description = "Nimble critter with venomous fangs."
        corpse = Enemies.CorpseSmall
        super().__init__("Small Blob", description=description, corpse=corpse,  health=12, attacks=attacks)


class StatsBlobBase(EntityStatsBase):
    def __init__(self):
        attacks = [Slam()]
        description = "Nimble critter with venomous fangs."
        corpse = Enemies.Corpse
        super().__init__("Blob", description=description, corpse=corpse,  health=24, attacks=attacks, size=2)


class StatsSpitterBase(EntityStatsBase):
    def __init__(self):
        attacks = [Spit()]
        description = "Nimble critter with venomous fangs."
        corpse = Enemies.CorpseSmall
        super().__init__("Spitter", description=description, corpse=corpse,  health=9, attacks=attacks)


class StatsBat(EntityStatsBase):
    def __init__(self):
        description = "Small flying critter with sharp fangs."
        corpse = Enemies.CorpseSmall
        super().__init__("Bat", description=description, corpse=corpse,  health=11)


class StatsAlbinoBat(EntityStatsBase):
    def __init__(self):
        description = "Flying critter with sharp fangs."
        corpse = Enemies.CorpseSmall
        super().__init__("Albino Bat", description=description, corpse=corpse,  health=24)


class StatsShroomite(EntityStatsBase):
    def __init__(self):
        description = "Large walking mushroom with a surprisingly robust cap."
        corpse = Enemies.CorpseSmall
        super().__init__("Shroomite", description=description, corpse=corpse,  health=16)


class StatsToadstool(EntityStatsBase):
    def __init__(self):
        description = "Old shroomite which has rooted itself someplace dank."
        corpse = Enemies.Corpse
        super().__init__("Toadstool", description=description, size=2, corpse=corpse,  health=46)


class StatsMudslinger(EntityStatsBase):
    def __init__(self):
        description = "Glob of mud. You're not sure whether there's something inside of it."
        corpse = Enemies.CorpseSmall
        super().__init__("Mudslinger", description=description, corpse=corpse,  health=14, shield=5, defaultForceBlock=2)


class StatsRotBlobSmall(EntityStatsBase):
    def __init__(self):
        attacks = [Slam()]
        description = ""
        corpse = Enemies.CorpseSmall
        super().__init__("Small Rot Blob", description=description, corpse=corpse,  health=22, attacks=attacks)


class StatsHobBlobSmall(EntityStatsBase):
    def __init__(self):
        attacks = [Slam()]
        description = ""
        corpse = Enemies.CorpseSmall
        super().__init__("Small Hob Blob", description=description, corpse=corpse,  health=34, attacks=attacks)


class StatsSprigat(EntityStatsBase):
    def __init__(self):
        description = "Living bark known for its regenerative abilities"
        corpse = Enemies.CorpseSmall
        buffs = {"regeneration": 5}
        super().__init__("Sprigat", description=description, corpse=corpse,  health=31, metabolism=1, defaultForceBlock=1, buffs=buffs)


# Corpses
_corpseArgs = {'isCorpse': True}


class StatsCorpseSmallBase(EntityStatsBase):
    def __init__(self):
        description = "The remains of a dead thing."
        super().__init__("Corpse", description=description,  health=3, **_corpseArgs)


class StatsCorpseBase(EntityStatsBase):
    def __init__(self):
        description = "The remains of a dead thing."
        super().__init__("Corpse", description=description,  health=5, **_corpseArgs)

