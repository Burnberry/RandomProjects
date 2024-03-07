from Code.Logic.Path import Path
from Code.Logic.GameMap import GameMap


def test_map(batch, camera):
    # Example map creation, edit each level
    w0, w = -1, 17
    h0, h = -1, 12
    dw, dh = 0, 0

    castle = (8, 1)
    start = (8, 9)
    tx, ty = 8, 5

    positions = [start]
    cur = start
    while cur != (8, 6):
        x, y = cur
        y -= 1
        cur = (x, y)
        positions.append(cur)
    while cur != (11, 6):
        x, y = cur
        x += 1
        cur = (x, y)
        positions.append(cur)
    while cur != (11, 4):
        x, y = cur
        y -= 1
        cur = (x, y)
        positions.append(cur)
    while cur != (5, 4):
        x, y = cur
        x -= 1
        cur = (x, y)
        positions.append(cur)
    while cur != (5, 2):
        x, y = cur
        y -= 1
        cur = (x, y)
        positions.append(cur)
    while cur != (8, 2):
        x, y = cur
        x += 1
        cur = (x, y)
        positions.append(cur)
    while cur != (8, 1):
        x, y = cur
        y -= 1
        cur = (x, y)
        positions.append(cur)

    path = Path(positions)
    return GameMap([path], [], batch, camera, w, h, w0, h0, dw, dh)