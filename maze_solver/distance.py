import math

def manhattan(a,b):
    x1,y1 = a
    x2,y2 = b

    return abs(x1-x2) + abs(y1 - y2)

def euclidean(a,b):
    x1,y1 = a
    x2,y2 = b

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def chebyshev(a,b):
    x1,y1 = a
    x2,y2 = b

    return max(abs(x1-x2), abs(y1-y2))
