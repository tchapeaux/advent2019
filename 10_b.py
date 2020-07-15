from _lib import getLinesForDay, manhattanDistance
import math

# This is a code I found on the web
def hcfnaive(a,b): 
    if(b==0): 
        return a 
    else: 
        return hcfnaive(b,a%b) 

myInput = getLinesForDay(10)

asteroids = set()

for y, row in enumerate(myInput):
    for x, cell in enumerate(row):
        if cell == '#':
            asteroids.add((x, y))

WIDTH = max([a[0] for a in asteroids]) + 1  # +1 because 0
HEIGHT = max([a[1] for a in asteroids]) + 1  # +1 because 0

# PART B

bestLocation = (20, 21)  # Taken right from part A
assert bestLocation in asteroids

# So here's what I think
# We have 247 visible asteroids from bestLocation
# So that means the 200th will be destroyed during the FIRST rotation
# right? (RIGHT ?????)
# it seems to make sense anyway
# so I just need to get the list of reachable asteroids
# and order them based on their angles
# and voila???

# mark all hidden asteroids
hidden = set()

# Sort other asteroids by manhattan distance
hidingAsteroidList = sorted(
    [ a for a in asteroids if a != bestLocation ],
    key=lambda a : manhattanDistance(bestLocation[0], bestLocation[1], a[0], a[1])
)

# same code as part a except we compile the list of visible at the end
for hidingAsteroid in hidingAsteroidList:
    # print "\thidingAsteroid", hidingAsteroid

    if hidingAsteroid in hidden:
        continue

    dist = (hidingAsteroid[0] - bestLocation[0], hidingAsteroid[1] - bestLocation[1])
    ratio = abs(hcfnaive(dist[0], dist[1]))  # maybe we can do it without the abs but it hurts my brain
    dist_step = (dist[0] / ratio, dist[1] / ratio)

    # print "\tdist", dist, "\tratio", ratio, "\tdist_step", dist_step

    # Trace a line from hidingAsteroid outwards and mark all encountered asteroids
    current_cell = hidingAsteroid
    while 0 <= current_cell[0] < WIDTH and 0 <= current_cell[1] < HEIGHT:
        new_cell = (current_cell[0] + dist_step[0], current_cell[1] + dist_step[1])
        # print "\t\t\tlooking at", new_cell
        if new_cell in asteroids and new_cell not in hidden:
            # print "\t\t\t\thides", new_cell
            hidden.add(new_cell)
        current_cell = new_cell

# Count remaining asteroids and attribute that as score
visibles = asteroids - hidden - { bestLocation }  # -1 because itself
# print "\ttotal score", asteroidsScore[possibleLocation]

# sort by angle between vertical and bestLocation

def getThatAngle(a):
    # get the angle with the positive X axis
    angle = math.atan2(a[1] - bestLocation[1], a[0] - bestLocation[0])
    print "\t", angle * (180 / math.pi)
    # get the angle with the positive Y axis (which interests us)
    angle = angle - math.pi / 2
    # for some reason i'm off by 180 degree
    angle -= math.pi / 2
    # hello this is me from the future
    # about that comment just above:
    # the 'for some reason' was that actually +Y is down here
    # silly me
    print "\t", angle * (180 / math.pi)
    angle = angle - math.pi / 2
    print "\t", angle * (180 / math.pi)
    # translate it to be between 0 and 2PI
    while angle < 0:
        angle += 2 * math.pi
    print "\t", angle * (180 / math.pi)
    return angle

sortedVisibles = sorted(visibles, key=getThatAngle)

for a in sortedVisibles:
    print a
    print getThatAngle(a) * (180 / math.pi)


# print sortedVisibles
print sortedVisibles[199]

# 523 (too low)
# 1119 (too low)
# (bugs are because maths are hard and my use of atan2 was not correct)
# 1919 (correct) => I was looking at sortedVisibles[200] when I needed to look at [199] ...
# no comment on that noobie mistake...

# Glad my 'it-seems-too-tricky' solution actually worked!
# I feel so clever now.