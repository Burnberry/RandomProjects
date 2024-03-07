class EntityStatsBase:
    """
    Data storage class for entity stats
    Allows for easy default values for different entities, so changing values can be delayed after testing
    """
    def __init__(self, name, description="", attacks=None, health=10, size=1, buffs=None, metabolism=0, shield=0, defaultForceBlock=0, corpse=None, isCorpse=False):
        self.name = name
        self.description = description
        self.maxHealth = health
        self.shield = shield
        self.size = size
        if buffs is None:
            buffs = []
        self.buffs = buffs
        self.metabolism = metabolism
        self.defaultForceBlock = defaultForceBlock
        if attacks is None:
            attacks = {}
        self.attacks = attacks
        self.corpse = corpse
        self.isCorpse = isCorpse
