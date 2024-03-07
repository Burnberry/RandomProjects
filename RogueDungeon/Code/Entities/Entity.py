from Code.Logic.Effects import *
from Code.Stats.AttackStatsBase import AttackStatsBase
from Code.Stats.EntityStats import *
from Code.Util.Assets import Img
from Code.Util.GameObject import SpriteGameObject, TextGameObject, HoverDisplay
from Code.Util.SettingsGlobal import SettingsGlobal


class Entity(SpriteGameObject):
    i = 0

    def __init__(self, scene, x, y, group=SpriteGameObject.Group.Foreground, anchor='bc', asset=Img.Box, entityData=None):
        super().__init__(scene, x, y, group, anchor, asset)
        self.stacks = {}
        """stack: (number, stackObject, numberObject)"""
        self.setEntityData(entityData)

        self.healthTag = TextGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tc", self.getText())
        self.attackDisplay = None
        self.effects = set()
        self.isAlive = True
        self.stunned = False
        self.corpse = None

        self.i = Entity.i
        Entity.i += 1

        self.goal = (0, 0)
        self.moveVector = (0, 0)
        self.goalSignal = None
        self.moveTime = 0

        # apply starter stacks
        if self.stats.shield > 0:
            self.setStack("block", self.stats.shield)
        if self.stats.defaultForceBlock > 0:
            self.setStack("forceBlock", self.stats.defaultForceBlock)
        for stack in self.stats.buffs:
            n = self.stats.buffs[stack]
            self.addStack(stack, n)

    def update(self, dt):
        for effect in list(self.effects):
            effect.update(dt)

        self.updateMovement(dt)

    def updateMovement(self, dt):
        if self.moveTime > 0:
            self.moveTime -= dt
            if self.moveTime <= 0:
                self.moveTime = 0
                self.setPosition(*self.goal)
                if self.goalSignal is not None:
                    self.goalSignal()
            else:
                dx, dy = self.moveVector
                x, y = self.getPosition()
                self.setPosition(x + dx * dt, y + dy * dt)

    def remove(self):
        self.healthTag.remove()
        for stack in list(self.stacks):
            _, obj, label = self.stacks[stack]
            obj.remove()
            label.remove()
        for effect in list(self.effects):
            effect.remove()
        if self.attackDisplay is not None:
            self.attackDisplay.remove()
        super().remove()

    def removeEffect(self, effect):
        self.effects.remove(effect)

    def removeStack(self, stack):
        if stack not in self.stacks:
            return
        _, obj, tag = self.stacks.pop(stack)
        obj.remove()
        tag.remove()
        self.orderObjects()

    def addEffect(self, effect):
        if not self.isAlive:
            return
        self.effects.add(effect)

    def addStack(self, stack, number):
        if not self.isAlive:
            return
        number += self.getStackCount(stack)

        if stack == "poison" or stack == "corrosion" or stack == "regeneration":
            poison, corrosion, regeneration = self.getStackCount("poison"), self.getStackCount("corrosion"), self.getStackCount("regeneration")
            if stack == "poison":
                poison = number
            elif stack == "corrosion":
                corrosion = number
            elif stack == "regeneration":
                regeneration = number
            poison, corrosion, regeneration = max(0, poison-regeneration), max(0, corrosion-regeneration), max(0, min(regeneration-poison, regeneration-corrosion))
            self.setStack("poison", poison)
            self.setStack("corrosion", corrosion)
            self.setStack("regeneration", regeneration)
            return

        self.setStack(stack, number)

    def getText(self):
        name = self.getName()
        if name == "Entity":
            name += str(self.i)
        health = max(0, self.maxHealth)
        return name + " " + str(self.health) + '/' + str(health)

    def getName(self):
        return "Entity"

    def getStackCount(self, stack):
        number, _, _ = self.stacks.get(stack, (0, 0, 0))
        return number

    def setPosition(self, x, y):
        super().setPosition(x, y)
        self.healthTag.setPosition(x, y)
        self.orderObjects()

    def setStack(self, stack, number):
        if not self.isAlive:
            return
        if number > 1:
            txt = str(number)
        else:
            txt = ""

        if number <= 0:
            self.removeStack(stack)
            return
        elif stack not in self.stacks:
            # create stack
            if stack == "poison":
                img = Img.StackPoison
                hoverText = "Poison Stack\nDeals piercing damage each turn"
            elif stack == "corrosion":
                img = Img.StackCorrosion
                hoverText = "Corrosion Stack\nDeals damage each turn"
            elif stack == "regeneration":
                img = Img.StackRegeneration
                hoverText = "Regeneration Stack\nHeals each turn"
            elif stack == "block":
                img = Img.StackBlock
                hoverText = "Block Stack\nBlocks incoming damage"
            elif stack == "forceBlock":
                img = Img.StackForceBlock
                hoverText = "Force Block Stack\nBlocks force based effects like stuns and pushing/pulling"
            elif stack == "dazed":
                img = Img.StackDazed
                hoverText = "Dazed Stack\nCreature is disoriented and can be pushed or stunned without force"
            elif stack == "stun":
                img = Img.StackStun
                hoverText = "Stun Stack\nCreature can't physically move and skips its turn"
            else:
                img = Img.Stack
                hoverText = "Undefined Stack"
            x, y = self.getPosition()
            obj = SpriteGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tl", img)
            tag = TextGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tl", txt)
            hoverDisplay = HoverDisplay(obj, hoverText)
        else:
            _, obj, tag = self.stacks[stack]
            tag.setText(txt)

        if number > self.getStackCount(stack):
            if stack == "poison":
                self.createPoisonEffect()
            elif stack == "corrosion":
                self.createCorrosionEffect()
            elif stack == "regeneration":
                self.createRegenerationEffect()
            elif stack == "block":
                self.createBlockEffect()
            elif stack == "forceBlock":
                self.createForceBlockEffect()
            elif stack == "dazed":
                self.createDazedEffect()
            elif stack == "stun":
                self.createStunEffect()

        self.stacks[stack] = (number, obj, tag)
        self.orderObjects()

    def setHealth(self, health):
        if not self.isAlive:
            return
        self.health = health
        if self.health <= 0:
            self.onDeath()
            if self.isRemoved():
                return
        self.healthTag.setText(self.getText())

    def setEntityData(self, entityStats):
        if entityStats is None:
            entityStats = StatsPlayerBase()
            print("improve Entity.set_entity_data() pls")
        self.maxHealth = entityStats.maxHealth
        self.health = self.maxHealth
        self.size = entityStats.size

        self.stats = entityStats

    def moveTo(self, x, y, time=0.3, f=None):
        self.moveTime = time
        dx, dy = self.getPosition()
        self.goal = (x, y)
        self.moveVector = ((x-dx)/time, (y-dy)/time)
        self.goalSignal = f

    def moveBattlePosition(self, movement):
        if movement == 0:
            return

        self.scene.moveEnemy(self, movement)
        return

    def orderObjects(self):
        if not self.isAlive:
            return
        self.orderStacks()

    def orderStacks(self):
        if not self.isAlive:
            return
        _, cy = self.healthTag.getAnchoredScreenPosition("bl")
        cx, _ = self.getAnchoredScreenPosition("bl")
        x, y = self.scene.game.camera.screenToGameCoords(cx, cy)

        for stack in self.stacks:
            _, obj, tag = self.stacks[stack]
            for o in [obj, tag]:
                o.setPosition(x, y)
                w, _ = o.getDimensions()
                x += w

    def onDeath(self):
        self.isAlive = False

    def onAttacked(self, attack: AttackStatsBase, attacker: 'Entity'):
        if not self.isAlive:
            return

        # damage
        damage = attack.damage
        if self.stats.isCorpse:
            damage += attack.force
        self.onDamage(damage, attack.pierceDamage)

        totalDamage = damage + attack.pierceDamage
        if attack.healthDrainLevel >= 1:
            health = min(attacker.health + totalDamage, attacker.stats.maxHealth)
            attacker.setHealth(health)
        if attack.healthDrainLevel == 2:
            attacker.setStack("regeneration", 3)

        # force
        self.onForceAttack(attack.force)

        # push/pull
        if abs(attack.push) > 0:
            if self.isAlive:
                self.onPushed(attack.push)
            elif self.corpse is not None:
                self.corpse.onPushed(attack.push, forcePush=True)

        # stun
        if attack.canStun:
            self.onStun()

        # other effects
        self.addStack("poison", attack.poison)
        self.addStack("corrosion", attack.corrosion)

    def onEnterTurn(self):
        if not self.isAlive:
            return
        self.stunned = self.getStackCount("stun") > 0
        self.onStacksTick()

    def onBuffs(self, buffs):
        if self.stats.isCorpse:
            return
        for buff in buffs:
            n = buffs[buff]
            self.addStack(buff, n)

    def onDamage(self, damage, pierceDamage=0):
        if damage <= 0 and pierceDamage <= 0:
            return
        block = self.getStackCount("block")
        block, damageLeftover = max(0, block-damage), max(0, damage-block)
        self.setStack("block", block)

        self.setHealth(self.health - (damageLeftover + pierceDamage))
        self.createDamageEffect(damage + pierceDamage)

    def onForceAttack(self, force):
        if self.stats.isCorpse:
            return
        forceBlock = self.getStackCount("forceBlock")
        dazed = self.getStackCount("dazed")

        force, forceBlock = max(0, force - forceBlock), max(0, forceBlock - force)
        # loop to create dazed stacks
        while force > 0:
            dazed += 1
            forceBlock += self.stats.defaultForceBlock + dazed
            force, forceBlock = max(0, force - forceBlock), max(0, forceBlock - force)

        self.setStack("forceBlock", forceBlock)
        self.setStack("dazed", dazed)

    def onPushed(self, push, forcePush=False):
        if self.stats.isCorpse and not forcePush:
            return
        if self.getStackCount("dazed") <= 0 and not forcePush:
            return
        if self.isRemoved():
            return

        # get pushed or pulled
        self.moveBattlePosition(push)

    def onStun(self):
        dazed = self.getStackCount("dazed")
        self.addStack("stun", dazed)
        self.setStack("dazed", 0)

    def onStacksTick(self):
        poison = self.getStackCount("poison")
        corrosion = self.getStackCount("corrosion")
        damage = corrosion
        if self.stats.isCorpse:
            damage += 1
        self.onDamage(damage, pierceDamage=poison)
        if poison > 0:
            self.createPoisonEffect()
            self.setStack("poison", poison - 1)
        if corrosion > 0:
            self.createCorrosionEffect()
            self.setStack("corrosion", corrosion - 1)

        regen = self.getStackCount("regeneration")
        if regen > 0:
            health = min(self.health+regen, self.stats.maxHealth)
            self.setHealth(health)
            self.createRegenerationEffect()
            self.setStack("regeneration", regen - 1)

        # force/daze/stun
        if self.getStackCount("stun") > 0:
            self.addStack("stun", -1)
        elif self.getStackCount("dazed") > 0:
            self.addStack("dazed", -1)

        if self.getStackCount("forceBlock") > self.stats.defaultForceBlock:
            self.addStack("forceBlock", -1)

        # entity abilities
        if self.stats.metabolism == 1:
            self.addStack("regeneration", 1)

    def createStackObject(self, img, n, color=None):
        x, y = self.getPosition()
        obj = SpriteGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tl", img)
        if color is not None:
            obj.setColor((127, 255, 191))
        tag = TextGameObject(self.scene, x, y, SpriteGameObject.Group.Text, "tl", n)
        return obj, tag

    def createDamageEffect(self, damage):
        if not self.isAlive:
            return
        if damage == 0:
            return
        effect = FloatingText(self, damage, scale=3)

    def createFloatingTextEffect(self, text, color=(0, 0, 0), ttl=0.5, speed=8, scale=1):
        effect = FloatingText(self, text, color=color, ttl=ttl, speed=speed, scale=scale)

    def createPoisonEffect(self):
        if not self.isAlive:
            return
        effect = Poison(self)

    def createCorrosionEffect(self):
        if not self.isAlive:
            return
        effect = GenericEffect(self, Img.StackCorrosion)

    def createRegenerationEffect(self):
        if not self.isAlive:
            return
        effect = GenericEffect(self, Img.StackRegeneration)

    def createBlockEffect(self):
        if not self.isAlive:
            return
        effect = GenericEffect(self, Img.StackBlock)

    def createForceBlockEffect(self):
        return
        #if not self.isAlive:
        #    return
        #effect = GenericEffect(self, Img.StackForceBlock)

    def createDazedEffect(self):
        if not self.isAlive:
            return
        effect = GenericEffect(self, Img.StackDazed)

    def createStunEffect(self):
        if not self.isAlive:
            return
        effect = GenericEffect(self, Img.StackStun)
