from constants import *

mouse_x = 0
mouse_y = 0

def compute_position(x, y):
    return (x * size_real + size_real // 2, y * size_real + size_real // 2)


def conventer(zoom, cx, cy, x, y):
    new_x = (cx - width / (2 * zoom)) + x / zoom
    new_y = cy - height / (2 * zoom) + y / zoom
    return new_x, new_y
