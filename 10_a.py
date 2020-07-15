from _lib import getLinesForDay, manhattanDistance

# This is a code I found on the web
def hcfnaive(a,b): 
    if(b==0): 
        return a 
    else: 
        return hcfnaive(b,a%b) 

myInput = getLinesForDay(10)

asteroids = set()

print myInput
for y, row in enumerate(myInput):
    for x, cell in enumerate(row):
        if cell == '#':
            asteroids.add((x, y))

WIDTH = max([a[0] for a in asteroids]) + 1  # +1 because 0
HEIGHT = max([a[1] for a in asteroids]) + 1  # +1 because 0

print WIDTH, HEIGHT

# Test all asteroids location
asteroidsScore = {}
for possibleLocation in asteroids:
    # print "possibleLocation", possibleLocation

    # mark all hidden asteroids
    hidden = set()

    # Sort other asteroids by manhattan distance
    hidingAsteroidList = sorted(
        [ a for a in asteroids if a != possibleLocation ],
        key=lambda a : manhattanDistance(possibleLocation[0], possibleLocation[1], a[0], a[1])
    )

    for hidingAsteroid in hidingAsteroidList:
        # print "\thidingAsteroid", hidingAsteroid

        if hidingAsteroid in hidden:
            continue

        # we need to find how often the line between possibleLocation and hidingAsteroid
        # crosses the grid.
        # I think this is linked to the gcd/hcf? (highest common factor)
        # like if the dist is (10, 15) we need to check every (2, 3) because the gcd is 5

        dist = (hidingAsteroid[0] - possibleLocation[0], hidingAsteroid[1] - possibleLocation[1])
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
    asteroidsScore[possibleLocation] = len(asteroids) - len(hidden) - 1  # -1 because itself
    # print "\ttotal score", asteroidsScore[possibleLocation]

print asteroidsScore
print max([(asteroidsScore[asteroid], asteroid) for asteroid in asteroidsScore])

# too high (hot damn): 250