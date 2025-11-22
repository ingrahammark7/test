import math
import random
import timeit

# ---------- Your method wrapped ----------
def geth_custom(x, y, x1, y1):
    if x1 == x and y1 == y:
        return 0
    difx = x1 - x
    dify = y1 - y
    if difx == 0 and dify > 0:
        return 90
    if difx == 0 and dify < 0:
        return 270
    if difx > 0 and dify == 0:
        return 0
    if difx < 0 and dify == 0:
        return 180
    ri = dify / difx
    res = ri * 45
    if x1 > x and y1 > y:
        if res > 90:
            res = 90
        return res
    if x1 < x and y1 > y:
        if res < -90:
            return 90
        return 180 + res
    if abs(res) > 90:
        return 270
    if x1 > x:
        return 360 + res
    return abs(res) + 180


# ---------- atan2 method ----------
def geth_atan2(x, y, x1, y1):
    dx = x1 - x
    dy = y1 - y
    if dx == 0 and dy == 0:
        return 0
    ang = math.degrees(math.atan2(dy, dx))
    return ang if ang >= 0 else ang + 360


# ---------- Prepare some random test data ----------
points = [(random.random()*1000, random.random()*1000,
           random.random()*1000, random.random()*1000)
          for _ in range(1000000)]  # 1 million


# ---------- Timing ----------
print("Custom method:",
      timeit.timeit(
          "for x,y,x1,y1 in points: geth_custom(x,y,x1,y1)",
          globals=globals(),
          number=1))

print("atan2 method:",
      timeit.timeit(
          "for x,y,x1,y1 in points: geth_atan2(x,y,x1,y1)",
          globals=globals(),
          number=1))