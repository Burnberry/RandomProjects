from Code.Logic.Runes import *


class Inventory:
    def __init__(self):
        self.loadInventory()

    def getDeck(self):
        """[(rune, n)] deck format"""
        return self.deck

    def getDeckCopy(self):
        """[(rune, n)] deck format"""
        return [] + self.getDeck()

    def getDeckDuplicates(self):
        """[rune] deck format, duplicates in deck possible"""
        deck = []
        for rune, n in self.deck:
            for _ in range(n):
                deck.append(rune)
        return deck

    def getDeckCount(self):
        x = 0
        for rune, n in self.deck:
            x += n
        return x

    def loadInventory(self):
        self._reset()
        self._loadDefault()

    def _reset(self):
        self.deck: list = []
        """List of CardObjects in current deck"""
        self.runes: dict[RuneObject: int] = {}
        """CardObject: int, Number of each rune in current inventory"""

    def _loadDefault(self):
        for n, rune in [(6, Spike), (4, MinorCorrosion), (2, Push), (2, Corrosion), (1, SpikeBlast)]:
            self.runes[rune] = n
            self.deck.append((rune, n))

    def deckCount(self, rune):
        for r, n in self.deck:
            if r == rune:
                return n
        return 0

    def runesCount(self, rune):
        return self.runes.get(rune, 0)

    def removeFromDeck(self, rune, amount=1):
        amount = min(amount, self.getDeckCount()-10)
        for i in range(len(self.deck)):
            r, n = self.deck[i]
            if r != rune:
                continue
            n -= amount

            if n <= 0:
                self.deck.pop(i)
            else:
                self.deck[i] = (rune, n)

            break

    def removeFromRunes(self, rune, amount=1):
        if rune not in self.runes:
            return
        n = self.runesCount(rune)
        n -= amount

        if n <= 0:
            del(self.runes[rune])
        else:
            self.runes[rune] = n

    def addToDeck(self, rune, amount=1):
        new = True
        for i in range(len(self.deck)):
            r, n = self.deck[i]
            if r != rune:
                continue
            new = False
            n += amount
            n = min(n, self.runesCount(rune))

            self.deck[i] = (rune, n)

            break

        if new:
            self.deck.append((rune, amount))

    def addToRunes(self, rune, amount=1):
        n = self.runesCount(rune)
        self.runes[rune] = n + amount

    def show(self):
        print(self.deck)
        print()
        print(self.runes)
