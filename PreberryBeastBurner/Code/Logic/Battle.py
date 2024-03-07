from Code.Utils.LinkedList import CircleLinkedList


class Battle:
    def __init__(self, entities):
        self.round = 0
        self.control = 0
        self.turnOrder = CircleLinkedList(entities)
        self.turnOrder.prev()
        self.entities = entities
        self.entitiesActive = self.get_next_active_group()

    def get_next_active_group(self):
        entities = [self.turnOrder.next()]
        self.control = entities[0].control
        #print("control change, #entities:", self.control, len(entities))
        for e in entities:
            e.AP, e.MP = e.maxAP, e.maxMP
        return entities

    def action(self, entity, AP, MP):
        # safety check
        if entity not in self.entitiesActive:
            print("Error:", entity.tag, " does not have its turn")
            return False
        if entity.MP < MP or entity.AP < AP:
            print("Error", entity.tag, "lacks resources, requires", AP, MP, "AP, MP and has", entity.AP, entity.MP)
            return False
        #self.end_turn(entity)
        #return True
        # Code for later
        entity.MP -= MP
        entity.AP -= AP
        if entity.MP + entity.AP == 0:
            self.end_turn(entity)
        return True

    def end_turn(self, entity):
        if entity in self.entitiesActive:
            self.entitiesActive.remove(entity)
        if len(self.entitiesActive) == 0:
            self.entitiesActive = self.get_next_active_group()

    def remove(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            self.turnOrder.remove_node(entity)
            if entity in self.entitiesActive:
                self.entitiesActive.remove(entity)

    def add(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)
            self.turnOrder.add(entity)
