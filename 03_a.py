import sys

from _lib import getLinesForDay, getCommaSeparatedLine, Grid, manhattanDistance

lines = getLinesForDay(3)
assert len(lines) == 2
cablesDescription = [getCommaSeparatedLine(l) for l in lines]


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

for (x, y) in getPoints(cablesDescription[0]):
    myGrid.set(x, y, 1)


# mark all grid cells with the 2nd cable, and mark intersections
intersections = []
for (x, y) in getPoints(cablesDescription[1]):
    if myGrid.get(x, y) == 1:
        intersections.append((x, y))
        myGrid.set(x, y, 3)
    else:
        myGrid.set(x, y, 2)

print "Intersections"
for inter in intersections:
    print inter

# Find closest intersection
closest_dist = sys.maxint
closest_point = None

for (x, y) in intersections:
    manhattan_dist = manhattanDistance(0, 0, x, y)
    if manhattan_dist < closest_dist:
        closest_dist = manhattan_dist
        closest_point = (x, y)

print closest_point, closest_dist