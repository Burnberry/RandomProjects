def rectilinear(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def rectidiagonal(x1, y1, x2, y2):
    return max(abs(x2 - x1), abs(y2 - y1))


def nearest_direction(x1, y1, x2, y2):
    x, y = 0, 0
    if abs(x2 - x1) <= abs(y2 - y1):
        dx = x2 - x1
        x = (dx > 0) - (dx < 0)
    else:
        dy = y2 - y1
        y = (dy > 0) - (dy < 0)
    return x, y
