from Code.Encounters.Encounters import Battle
from Code.Logic.Button import ButtonText, ButtonSprite
from Code.Util.GameObject import LineObject, TextGameObject, BoxObject, BaseButton
from Code.Util.Scene import Scene
from Code.Util.SettingsGlobal import SettingsGlobal


class MapScene(Scene):

    def __init__(self, game):
        super().__init__(game)

        self.encounterMap = self.game.encounterMap
        self.reachableEncounters = set(self.encounterMap.currentEncounter.iterateEncounters())
        self.path = set(self.encounterMap.path)

        self.state = self.getState()
        print(self.state)

        self.encounterButtons = []
        self.encounterConnections = []

        self.rewardUI = None
        self.rewardSelected = None
        self.createButtons()
        self.createMap()

        self.onEncounterNodePress(self.encounterMap.currentEncounter, force=True)
        if self.state == "reward":
            pass # self.createRewardScreen()

    def update(self, dt):
        pass

    def handleInput(self, dt):
        pass

    def getState(self):
        encounter = self.encounterMap.currentEncounter.encounter
        if encounter.completed:
            state = "travel"
        elif not encounter.battleCompleted:
            state = "battle"
        elif not encounter.rewardReceived:
            state = "reward"
        else:
            print("unknown map state")
            state = "unknown"
        return state

    def onEncounterNodePress(self, encounterNode, force=False):
        if self.state != "travel" and not force:
            return
        if encounterNode in self.encounterMap.currentEncounter.getEncounterPaths() or force:
            self.encounterMap.setCurrentEncounter(encounterNode)

            state = self.getState()
            if state == "battle":
                self.setSwitchState("BATTLE")
                self.game.saveData()
                return
            elif state == "reward":
                self.createRewardScreen()
            self.createMap()

    def onRewardSelect(self, i):
        _, _, rewards, _ = self.rewardUI

        self.rewardSelected = rewards[i]
        for reward in rewards:
            if reward is self.rewardSelected:
                reward.setColors((255, 255, 255), (255, 255, 255))
            else:
                reward.setColors((100, 100, 100), (200, 200, 200))

    def onRewardButtonPress(self, arg):
        if self.rewardSelected is None:
            return
        reward = type(self.rewardSelected.gameVisualObject)

        if arg == "deck":
            self.game.inventory.addToRunes(reward)
            self.game.inventory.addToDeck(reward)
        elif arg == "bag":
            self.game.inventory.addToRunes(reward)
        else:
            print("unexpected arg in onRewardButtonPress")

        self.encounterMap.currentEncounter.encounter.receiveReward()
        self.state = self.getState()

        self.game.saveData()

        self.clearRewardScreen()

    def createMap(self):
        self.clearMap()

        self.reachableEncounters = set(self.encounterMap.currentEncounter.iterateEncounters())
        self.path = set(self.encounterMap.path)

        for depth in self.encounterMap.startEncounter.iterateEncountersPerDepth():
            for encounter in depth:
                self.createEncounterButton(encounter)
                for encounter2 in encounter.getEncounterPaths():
                    self.createEncounterConnection(encounter, encounter2)

    def createRewardScreen(self):
        # remove old if exists
        self.clearRewardScreen()

        encounter = self.encounterMap.currentEncounter.encounter
        anchor = "bl"

        rewardText = TextGameObject(self, 0, 0, TextGameObject.Group.Popup, anchor, "Choose a reward")
        rewards = []
        for i, reward in enumerate(encounter.reward.rewards):
            runeObj = reward(self, 0, 0, group=TextGameObject.Group.Popup, anchor=anchor)
            rewards.append(BaseButton(runeObj, self.onRewardSelect, args=(i,)))

        # reward buttons
        toDeck = ButtonText(self, 0, 0, anchor, "to deck", self.onRewardButtonPress, ("deck",), group=TextGameObject.Group.Popup)
        toRunes = ButtonText(self, 0, 0, anchor, "to bag", self.onRewardButtonPress, ("bag",), group=TextGameObject.Group.Popup)
        rewardButtons = [toDeck, toRunes]

        dx, dy = 2, 1
        dcx, dcy = dx*SettingsGlobal.Scale, dy*SettingsGlobal.Scale

        cw1, ch1 = rewardText.getScreenDimensions()
        cw1 += dcx
        cw2, ch2 = 0, 0
        for reward in rewards:
            cw, ch = reward.gameVisualObject.getScreenDimensions()
            ch2 = max(ch2, ch)
            cw2 += cw + dcx
        cw3, ch3 = 0, 0
        for rewardButton in rewardButtons:
            cw, ch = rewardButton.gameVisualObject.getScreenDimensions()
            ch3 = max(ch3, ch)
            cw3 += cw + dcx*5

        cw = max(cw1, cw2, cw3) + dcx
        ch = ch1 + ch2 + ch3 + 6*dcy

        x, y = self.game.camera.getCenter()
        rewardBackground = BoxObject(self, x, y, BoxObject.Group.PopupBackground, "cc", cw, ch, color=(10, 20, 40), screenDimensions=True)

        # set positions of UI
        x0, y0 = rewardBackground.getAnchoredPosition(anchor)
        x0 += dx
        y0 += dy
        x, y = x0, y0

        h = 0
        for rewardButton in rewardButtons:
            rewardButton.gameVisualObject.setPosition(x, y)
            w0, h0 = rewardButton.gameVisualObject.getDimensions()
            x += w0 + dx*5
            h = max(h, h0)
        x = x0
        y += h + dy

        h = 0
        for reward in rewards:
            reward.gameVisualObject.setPosition(x, y)
            w0, h0 = reward.gameVisualObject.getDimensions()
            x += w0 + dx
            h = max(h, h0)
        x = x0
        y += h + dy

        rewardText.setPosition(x, y)

        self.rewardUI = rewardBackground, rewardText, rewards, rewardButtons

        self.rewardSelected = None
        if len(rewards) == 1:
            self.onRewardSelect(rewards[0])

    def createEncounterConnection(self, encounter1, encounter2):
        x1, y1 = encounter1.getPosition()
        x2, y2 = encounter2.getPosition()
        connection = LineObject(self, x1, y1+2, x2, y2-2, LineObject.Group.Foreground)
        if encounter1 is self.encounterMap.currentEncounter:
            color = (127, 127, 0)
        elif encounter2 in self.reachableEncounters:
            color = (127, 127, 127)
        elif encounter1 in self.path and encounter2 in self.path:
            color = (140, 100, 20)
        else:
            color = (50, 50, 50)
        connection.setColor(color)
        self.encounterConnections.append(connection)

    def createEncounterButton(self, encounter):
        x, y = encounter.getPosition()
        button = ButtonText(self, x, y, 'cc', encounter.getName(), self.onEncounterNodePress, (encounter,))

        if encounter in self.path:
            button.setColors((140, 100, 20), (140, 100, 20))
        elif encounter not in self.reachableEncounters:
            button.setColors((20, 20, 20), (20, 20, 20))
        elif encounter not in self.encounterMap.currentEncounter.getEncounterPaths():
            button.setColors((60, 60, 60), (60, 60, 60))
        self.encounterButtons.append(button)

    def createButtons(self):
        self.deckLeftButton, self.deckRightButton, self.runesLeftButton, self.runesRightButton = None, None, None, None
        x, y = self.game.camera.getCenter()
        self.backButton = ButtonText(self, 280, 160+8, 'cc', "MAIN", self.setSwitchState, ("MAIN",))
        self.deckButton = ButtonText(self, 280, 160-8, 'cc', "DECK", self.setSwitchState, ("DECK",))

        self.backButton.setScale(3)
        self.deckButton.setScale(3)

    def clearEncounterButtons(self):
        for button in self.encounterButtons:
            button.remove()

    def clearMap(self):
        for button in self.encounterButtons:
            button.remove()
        self.encounterButtons = []

        for connection in self.encounterConnections:
            connection.remove()
        self.encounterConnections = []

    def clearRewardScreen(self):
        if self.rewardUI is not None:
            rewardBackground, rewardText, rewards, rewardButtons = self.rewardUI
            for obj in [rewardBackground, rewardText] + rewards + rewardButtons:
                obj.remove()
