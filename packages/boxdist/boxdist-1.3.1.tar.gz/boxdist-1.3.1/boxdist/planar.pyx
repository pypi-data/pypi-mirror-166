def planar_box_dist(
    px: float,
    py: float,
    minx: float,
    miny: float,
    maxx: float,
    maxy: float,
) -> float:
    cdef double dx, dy

    if px < minx:
        dx = minx - px
    elif px <= maxx:
        dx = 0
    else:
        dx = px - maxx

    if py < miny:
        dy = miny - py
    elif py <= maxy:
        dy = 0
    else:
        dy = py - maxy

    return dx * dx + dy * dy
