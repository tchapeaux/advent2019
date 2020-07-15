## ADVENT OF CODE 2019 DAY 3
# We have a description of two cables in a grid, we must find where they intersects
# and single out the intersection which is closest to the start point of both cables

import sys

from _lib import getLinesForDay, getCommaSeparatedLine, Grid, manhattanDistance

lines = getLinesForDay(3)
assert len(lines) == 2
cablesDescription = [getCommaSeparatedLine(l) for l in lines]

cablesExample0 = [
    ["R8","U5","L5","D3"],
    ['U7','R6','D4','L4']
]

cablesExample1 = [
    ['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
    ['U62','R66','U55','R34','D71','R55','D58','R83']
]

cablesExample2 = [
    ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
    ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
]

def getPoints(cablePath):
    currentPointX = 0
    currentPointY = 0

    for cableNode in cablePath:
        direction = cableNode[0]
        length = int(cableNode[1:])

        if direction == 'U':
            for _y in range(length):
                yield (currentPointX, currentPointY - (_y + 1))
            currentPointY -= length
        elif direction == 'D':
            for _y in range(length):
                yield (currentPointX, currentPointY + (_y + 1))
            currentPointY += length
        elif direction == 'L':
            for _x in range(length):
                yield (currentPointX - (_x + 1), currentPointY)
            currentPointX -= length
        elif direction == 'R':
            for _x in range(length):
                yield (currentPointX + (_x + 1), currentPointY)
            currentPointX += length

myGrid = Grid()

# mark all grid cells where the first cable goes through
# note: if a cable goes multiple times through a cell, only keep the first step count
# note2: enumerate starts at 0, so we need to +1
for step1, (x, y) in enumerate(getPoints(cablesDescription[0])):
    if (not myGrid.get(x, y)):
        myGrid.set(x, y, step1 + 1)

# follow cable 2 and mark intersections
# note: we do not mark grid cells where cable 2 goes because
# 1 - we do not care
# 2 - that would make us count self-intersection as intersections, which we do not want
intersections = []
for step2, (x, y) in enumerate(getPoints(cablesDescription[1])):
    step1 = myGrid.get(x, y)
    if step1:
        intersections.append((x, y, step1 + step2 + 1))

print "Intersections"
for inter in intersections:
    print inter

# Find closest intersection
closest_dist = sys.maxint
closest_point = None

for (x, y, combined_dist) in intersections:
    if combined_dist < closest_dist:
        closest_dist = combined_dist
        closest_point = (x, y)

print "Closest"
print closest_point, closest_dist

# 7520 too low (error was: I was counting a self-intersection)