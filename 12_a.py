from itertools import combinations
import re

from _lib import getLinesForDay

rawInput = getLinesForDay(12)

planets = [{} for l in rawInput]
for idx, line in enumerate(rawInput):
    coords = re.match(r"<x=(.*), y=(.*), z=(.*)>", line).groups()
    planets[idx]['pos'] = [ int(c) for c in coords ]
    planets[idx]['vel'] = [0, 0, 0]

NB_OF_STEPS = 1000

def showPlanets(planets):
    for p in planets:
        print "pos=", p['pos'], 'vel=', p['vel']

for step in range(NB_OF_STEPS):
    print "step", step
    showPlanets(planets)

    # Take each couple to update velocity based on gravity
    for (planet1, planet2) in combinations(planets, 2):
        # same logic for x, y, z coordinates
        for coord in range(3):
            if planet2['pos'][coord] > planet1['pos'][coord]:
                planet1['vel'][coord] += 1
                planet2['vel'][coord] -= 1
            elif planet2['pos'][coord] < planet1['pos'][coord]:
                planet1['vel'][coord] -= 1
                planet2['vel'][coord] += 1
            else:
                assert planet1['pos'][coord] == planet2['pos'][coord]

    # Update pos based on velocity
    for planet in planets:
        for coord in range(3):
            planet['pos'][coord] += planet['vel'][coord]

print "step", NB_OF_STEPS
showPlanets(planets)

energySum = 0
for p in planets:
    potEnergy = 0
    for v1 in p['pos']:
        potEnergy += abs(v1)

    kinEnergy = 0
    for v2 in p['vel']:
        kinEnergy += abs(v2)

    energySum += potEnergy * kinEnergy

print energySum

print planets

# wrong guesses
# 34 (too low)
# ok i was not computing energy correctly at all : forgot absolute value and summed the two type instead of multiplying
