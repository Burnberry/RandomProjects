from copy import deepcopy
from random import shuffle, randint

from Code.Entities import *
from Code.Logic.ActionType import ActionType
from Code.Logic.Actions.ActionSequence import ActionSequence
from Code.Logic.Actions.BaseAttackAction import BaseAttackAction
from Code.Logic.Actions.MoveAction import MoveAction
from Code.Logic.Checks import *
from Code.Logic.MovementType import MovementType
from Code.Utils.Distance import *


class BaseAI:
    def __init__(self, entity, area, gamelogic):
        self.Entity = entity
        self.Area = area
        self.Target = None
        self.GameLogic = gamelogic

    def do_action(self):
        # Check for target
        if self.Target is None:
            self.get_target()
        elif not self.Target.Alive:
            self.get_target()

        if self.Target is None:
            return self.action_random()
        else:
            if self.in_attack_range():
                if self.Entity.AP >= 1:
                    return self.action_attack()
                else:
                    self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
                    return True
            elif self.Entity.MP >= 1:
                return self.action_move()
            else:
                self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
                return True
        return False

    def action_random(self):
        # Do nothing 75% chance
        if randint(0, 15) < 6:
            self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
            return False

        actions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        shuffle(actions)
        x, y = self.Entity.x, self.Entity.y
        for dx, dy in actions:
            if valid_move(self.Area, self.Entity, x, y, dx, dy, MovementType.WALK):
                # Do action
                self.GameLogic.action(self.Entity, ActionType.MOVE, x + dx, y + dy)
                self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
                return True

        # No movement possible
        self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
        return False

    def action_attack(self):
        # do action
        x, y = self.Target.x, self.Target.y
        self.GameLogic.action(self.Entity, ActionType.ATTACK, x, y)
        return True

    def in_attack_range(self):
        r = 1
        x1, y1 = self.Entity.x, self.Entity.y
        x2, y2 = self.Target.x, self.Target.y

        return rectidiagonal(x1, y1, x2, y2) <= r

    def action_move(self):
        # path[0], path[-1] = current position, destination
        path = self.get_best_path()

        if path is None:
            return False
        if len(path) <= 1:
            self.GameLogic.action(self.Entity, ActionType.END_TURN, 0, 0)
            print("Path too short", path)
            return False

        # Do action based on path
        # temp, move range is 1, so only pick first movement
        x, y = path[1]
        self.GameLogic.action(self.Entity, ActionType.MOVE, x, y)
        return True

    def get_best_path(self, goal=None, distance_allowed_from_goal=1, limit=16):
        start = (self.Entity.x, self.Entity.y)
        if goal is None:
            goal = (self.Target.x, self.Target.y)

        open_nodes = set()
        open_nodes.add(start)
        cur_score = {start: 0}
        est_score = {start: rectilinear(*start, *goal)}
        prev_node = {}

        current_nodes = []

        while len(open_nodes) > 0:
            # Get minimum score nodes: current_nodes
            # Also check if goal was reached
            min_score = limit
            end_node = None
            for node in open_nodes:
                score = cur_score[node] + est_score[node]
                if score < min_score:
                    min_score = score
                    current_nodes = []
                    end_node = None
                if score == min_score:
                    current_nodes.append(node)
                    if rectilinear(*node, *goal) <= distance_allowed_from_goal:
                        end_node = node

            if end_node:
                # reconstruct path
                path = [end_node]
                current_node = end_node
                while current_node != start:
                    current_node = prev_node[current_node]
                    path.append(current_node)

                return path[::-1]
            if min_score >= limit:
                # Limit reached, search no longer
                return None
            for node in current_nodes:
                x, y = node
                neighbors = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
                d_score = cur_score[node] + 1
                for neighbor in neighbors:
                    dx, dy = neighbor[0] - x, neighbor[1] - y
                    if not valid_move(self.Area, self.Entity, x, y, dx, dy, MovementType.WALK):
                        continue
                    if cur_score.get(neighbor, d_score+1) > d_score:
                        prev_node[neighbor] = node
                        cur_score[neighbor] = d_score
                        est_score[neighbor] = rectilinear(neighbor[0], neighbor[1], goal[0], goal[1])
                        open_nodes.add(neighbor)
                open_nodes.remove(node)
            current_nodes = []

        return None

    def get_target(self):
        sight_range = 7
        x, y = self.Entity.x, self.Entity.y
        target = None
        for i in range(1, sight_range+1):  # Check nearest tiles first
            dx, dy = i, 0
            for _ in range(i):
                dx -= 1
                dy += 1
                if self.valid_target(x+dx, y+dy):
                    target = self.Area.getTile(x+dx, y+dy).getEntity()
                    break
            for _ in range(i):
                dx -= 1
                dy -= 1
                if self.valid_target(x+dx, y+dy):
                    target = self.Area.getTile(x + dx, y + dy).getEntity()
                    break
            for _ in range(i):
                dx += 1
                dy -= 1
                if self.valid_target(x+dx, y+dy):
                    target = self.Area.getTile(x + dx, y + dy).getEntity()
                    break
            for _ in range(i):
                dx += 1
                dy += 1
                if self.valid_target(x+dx, y+dy):
                    target = self.Area.getTile(x + dx, y + dy).getEntity()
                    break
        self.Target = target

    def valid_target(self, x, y):
        if self.Area.inside_area(x, y):
            e = self.Area.getTile(x, y).getEntity()
            if e is not None:
                if e.Alive and isinstance(e, EntityGen.Player):
                    return True
        return False

    def get_basic_actions(self):
        # returns basic action options (move to or base attack)
        attack_actions = self.get_attack_actions()
        move_actions = self.get_move_actions()

        actions = attack_actions + move_actions
        return actions

    def get_attack_actions(self):
        # Only returns tiles with an entity within reach
        # Current range is only 1
        if self.Entity.AP < 1:
            return []

        radius = 1
        actions = set()
        x, y = self.Entity.x, self.Entity.y

        for r in range(1, radius+1):
            dx, dy = r, r
            for _ in range(2*r):
                dx -= 1
                if not self.Area.inside_area(x+dx, y+dy):
                    continue
                target = self.Area.getTile(x+dx, y+dy).entity
                if target is not None:
                    action = BaseAttackAction(ActionType.ATTACK, self.Entity, target, x+dx, y+dy, self.Entity.damage)
                    actions.add(action)
            for _ in range(2*r):
                dy -= 1
                if not self.Area.inside_area(x+dx, y+dy):
                    continue
                target = self.Area.getTile(x + dx, y + dy).entity
                if target is not None:
                    action = BaseAttackAction(ActionType.ATTACK, self.Entity, target, x+dx, y+dy, self.Entity.damage)
                    actions.add(action)
            for _ in range(2*r):
                dx += 1
                if not self.Area.inside_area(x+dx, y+dy):
                    continue
                target = self.Area.getTile(x + dx, y + dy).entity
                if target is not None:
                    action = BaseAttackAction(ActionType.ATTACK, self.Entity, target, x+dx, y+dy, self.Entity.damage)
                    actions.add(action)
            for _ in range(2*r):
                dy += 1
                if not self.Area.inside_area(x+dx, y+dy):
                    continue
                target = self.Area.getTile(x + dx, y + dy).entity
                if target is not None:
                    action = BaseAttackAction(ActionType.ATTACK, self.Entity, target, x+dx, y+dy, self.Entity.damage)
                    actions.add(action)

        return list(actions)

    def get_move_actions(self):
        start = (self.Entity.x, self.Entity.y)

        open_set = set()
        explored = set()
        explored.add(start)
        open_set.add(start)

        limit = self.Entity.MP
        move_distance = 1
        actions = {start: ActionSequence([])}

        while len(open_set) > 0 and limit >= move_distance:
            next_open_set = set()
            for tile in open_set:
                x, y = tile
                neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                for neighbor in neighbors:
                    dx, dy = neighbor
                    new_tile = (x + dx, y + dy)
                    if new_tile not in explored:
                        if valid_move(self.Area, self.Entity, x, y, dx, dy, MovementType.WALK):
                            next_open_set.add(new_tile)
                            explored.add(new_tile)
                            move_action = MoveAction(ActionType.MOVE, self.Entity, x+dx, y+dy)
                            action = ActionSequence(actions[tile].actions + [move_action])
                            actions[(x+dx, y+dy)] = action
            open_set = next_open_set

            # Next iteration, explore one extra distance
            move_distance += 1

        del(actions[start])  # remove empty move sequence
        return list(actions.values())
