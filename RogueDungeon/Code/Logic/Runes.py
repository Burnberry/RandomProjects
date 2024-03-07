from Code.Logic.RuneObject import RuneObject
from Code.Stats.RuneStats import *
from Code.Util.Assets import Img


class Spike(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsSpike()
        super().__init__(scene, x, y, stats=stats, asset=Img.Spike, group=group, anchor=anchor)


class SpikeBlast(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsSpikeBlast()
        super().__init__(scene, x, y, stats=stats, asset=Img.SpikeBlast, group=group, anchor=anchor)


class MinorCorrosion(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsMinorCorrosion()
        super().__init__(scene, x, y, stats=stats, asset=Img.MinorCorrosion, group=group, anchor=anchor)


class Corrosion(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsCorrosion()
        super().__init__(scene, x, y, stats=stats, asset=Img.Corrosion, group=group, anchor=anchor)


class CorrosiveSpray(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsCorrosiveSpray()
        super().__init__(scene, x, y, stats=stats, asset=Img.CorrosiveSpray, group=group, anchor=anchor)


class Push(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsPush()
        super().__init__(scene, x, y, stats=stats, asset=Img.Push, group=group, anchor=anchor)


class BoulderBash(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsBoulderBash()
        super().__init__(scene, x, y, stats=stats, asset=Img.BoulderBash, group=group, anchor=anchor)


class StoneHail(RuneObject):
    def __init__(self, scene, x, y, group=RuneObject.Group.Foreground, anchor="bc"):
        stats = RuneStatsStoneHail()
        super().__init__(scene, x, y, stats=stats, asset=Img.StoneHail, group=group, anchor=anchor)


# legacy runes
class Attack1(RuneObject):
    def __init__(self, scene, x, y):
        stats = RuneStatsBaseBasicAttack()
        super().__init__(scene, x, y, stats=stats, asset=Img.Attack1)


class Attack2(RuneObject):
    def __init__(self, scene, x, y):
        stats = RuneStatsBaseSmash()
        super().__init__(scene, x, y, stats=stats, asset=Img.Attack2)


class Poison1(RuneObject):
    def __init__(self, scene, x, y):
        stats = RuneStatsBasePoisonBlast()
        super().__init__(scene, x, y, stats=stats, asset=Img.Poison1)


class Push1(RuneObject):
    def __init__(self, scene, x, y):
        stats = RuneStatsBasePush()
        super().__init__(scene, x, y, stats=stats, asset=Img.Push1)
