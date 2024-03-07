from numpy.random import choice

from Code.Util.Iter import Iter
from Code.Util import Assets
from Code.Logic.Line import Line
from Code.Logic.LineSet import LineSet


def new_tag(tags):
    tag = Iter.i()
    tags.add(tag)
    return tag


def normalize_p(subject):
    s = sum(subject.values())
    return {key: subject[key] / s for key in subject}


class LineGenerator:
    tags = set()
    subjects = dict()

    # define tags
    default = new_tag(tags)
    peasant = new_tag(tags)
    bat = new_tag(tags)

    line_library = {
        default: [
            'appeal', 'fat', 'yard', 'wear', 'sport', 'plant', 'pier', 'thread', 'elect', 'fog', 'bean', 'deport', 'brick', 'veil', 'drown', 'call', 'delete', 'medium', 'lace', 'skate', 'lion', 'banner', 'drop', 'pen', 'fault', 'dump', 'swarm', 'vote', 'paint', 'half', 'bride', 'store', 'hover', 'cream', 'depart', 'pace', 'gloom', 'rage', 'gain', 'bomber', 'spirit', 'add', 'begin', 'team', 'refer', 'hard', 'fur', 'cheque', 'style', 'ear', 'visual', 'cereal', 'low', 'jungle', 'bite', 'flash', 'trunk', 'pipe', 'frog', 'refer', 'time', 'coerce', 'lazy', 'crude', 'reduce', 'sound', 'sum', 'berry', 'behave', 'bare', 'rise', 'roll', 'debt', 'kick', 'rest', 'kettle', 'hide', 'voter', 'import', 'poll', 'slot', 'beer', 'coma', 'burial', 'betray', 'speech', 'rider', 'occupy', 'green', 'van', 'kill', 'tough', 'ferry', 'dealer', 'beam', 'lung', 'grace', 'learn', 'valley', 'bee', 'earwax', 'stress', 'file', 'raise', 'scale', 'glory', 'crop', 'mosque', 'bin', 'child', 'spoil', 'virus', 'brave', 'proof', 'rent', 'shadow', 'speed', 'sell', 'curve', 'palace', 'noble', 'need', 'rank', 'is', 'real', 'solo', 'obese', 'evoke', 'object', 'season', 'pour', 'bet', 'sale', 'debt', 'we', 'misery', 'reduce', 'arrest', 'hold', 'mask', 'good', 'brag', 'weapon', 'orgy', 'mobile', 'stock', 'free', 'guess', 'time', 'sting', 'crash', 'trail', 'foot', 'maid', 'side', 'pony', 'lazy', 'poem', 'corner', 'eaux', 'TRUE', 'turkey', 'tablet', 'prize', 'sow', 'touch', 'faint', 'owl', 'reach', 'loop', 'size', 'poison', 'knock', 'blonde', 'summer', 'sting', 'sign', 'key', 'sugar', 'queue', 'block', 'thread', 'salon', 'sit', 'peace', 'slave', 'awful', 'bury', 'system', 'object', 'nature', 'jewel', 'revive', 'death', 'rent', 'jail', 'speech', 'empire', 'piece', 'glow'
        ],
        peasant: [
            'peasant', 'pleb', 'scrub', 'village', 'nitwit', 'bread', 'grain', 'shoddy', 'plain', 'simple', 'farmer', 'pitchfork', 'haystack', 'shepherd', 'poor', 'illiterate', 'potato', 'hungry', 'famine', 'starving', 'lowborn', 'commoner', 'inferior', 'torch', 'stench', 'manure'
        ],
        bat: [
            'bat', 'wings', 'fangs', 'blood', 'vampire', 'drains', 'mammal', 'cave', 'darkness', 'dusk', 'screeches', 'echolocation', 'blind', 'rabies', 'swoop'
        ]
    }

    # define subjects, add weights to tags for chance of tag being chosen
    subjects[Assets.Creature.Peasant0] = {
        default: 1
    }
    subjects[Assets.Creature.Peasant1] = {
        peasant: 1
    }
    subjects[Assets.Creature.Bat] = {
        bat: 1
    }
    subjects[default] = {default: 1}

    # Line sets, needs to be initialized
    line_sets = {}
    for tag in tags:
        lines = line_library.get(tag, [])
        line_set = LineSet(lines)
        line_sets[tag] = line_set

    # Normalize subjects
    for key in subjects:
        subjects[key] = normalize_p(subjects[key])

    def __init__(self):
        pass

    def generate_line(self, subject=default):
        tag = self.subject_to_tag(subject)
        line = self.retrieve_line(tag)
        return line

    def retrieve_line(self, tag):
        line = self.line_sets[tag].next_line(Line.activeLines)
        if not line:
            print("Error, no valid line with tag", tag)
            line = self.line_sets[self.default].next_line(Line.activeLines)
        return line

    def subject_to_tag(self, subject):
        tag_dict = self.subjects[subject]
        tag = choice(list(tag_dict.keys()), p=list(tag_dict.values()))
        return tag
