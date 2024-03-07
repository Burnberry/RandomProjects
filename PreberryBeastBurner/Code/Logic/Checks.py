def valid_move(area, entity, x, y, dx, dy, movement_type):
    if area.inside_area(x+dx, y+dy):
        tile = area.getTile(x+dx, y+dy)
        return tile.entity is None
    return False


def valid_attack(area, entity, x, y, dx, dy, attack_type):
    return True
