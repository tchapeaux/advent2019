from copy import deepcopy
from itertools import combinations
import math
import re

from _lib import getLinesForDay

rawInput = getLinesForDay(12)

# Each planet is a list with 6 elements:
# x, y, z, vx, vy, vz
planets = [[] for l in rawInput]

for idx, line in enumerate(rawInput):
    coords = re.match(r"<x=(.*), y=(.*), z=(.*)>", line).groups()
    planets[idx] = [ int(c) for c in coords ]
    planets[idx] += [0, 0, 0]

planetsInit = deepcopy(planets)

def showPlanets(planets):
    for p in planets:
        print "pos=", p[:3], 'vel=', p[3:6]

# PART B
# The trick here is that each position is independent
# i.e. x, y, z each updates independetly of the others
# So we can find the period in each axis then return the LCM
# In all honesty: I had to look it up
# Still: it's fun to implement it

x_period = None
y_period = None
z_period = None

print "initial planets positions"
showPlanets(planets)

step = 0
while any([ p is None for p in [x_period, y_period, z_period] ]):
    step += 1

    if step % 1000000 == 0:
        print "step", '{:,}'.format(step)
        showPlanets(planets)

    # Take each couple to update velocity based on gravity
    for (planet1, planet2) in combinations(planets, 2):
        # same logic for x, y, z coordinates
        for coord in range(3):
            if planet2[coord] > planet1[coord]:
                planet1[3 + coord] += 1
                planet2[3 + coord] -= 1
            elif planet2[coord] < planet1[coord]:
                planet1[3 + coord] -= 1
                planet2[3 + coord] += 1
            else:
                assert planet1[coord] == planet2[coord]

    # Update pos based on velocity
    for planet in planets:
        for coord in range(3):
            planet[coord] += planet[3 + coord]

    # Check for periodicity
    if not x_period and all([ (p1[0] == p2[0] and p1[3] == p2[3]) for p1, p2 in zip(planets, planetsInit) ]):
        print "FOUND X PERIOD", step
        showPlanets(planets)
        x_period = step
    if not y_period and all([ (p1[1] == p2[1] and p1[4] == p2[4]) for p1, p2 in zip(planets, planetsInit) ]):
        print "FOUND Y PERIOD", step
        showPlanets(planets)
        y_period = step
    if not z_period and all([ (p1[2] == p2[2] and p1[5] == p2[5]) for p1, p2 in zip(planets, planetsInit) ]):
        print "FOUND Z PERIOD", step
        showPlanets(planets)
        z_period = step


print "---"
print "took", step, "steps"

print "periods:", x_period, y_period, z_period

# This gives us 268296 113028 231614

# Find lcm
# Naive implementation
def lcm(a, b, c):
    steps = [a, b, c]
    accum = [a, b, c]

    while not (accum[0] == accum[1] == accum[2]):
        greatestAccum = max(accum)
        for idx in range(3):
            if accum[idx] < greatestAccum:
                accum[idx] += steps[idx]

    return accum[0]

# print lcm(x_period, y_period, z_period)

# This actually takes a long time
# So during that time I asked Wolfram Alpha
# LCM = 292 653 556 339 368  (292 trillions)
# It is said that my python process is still looping to this day

# Ok so I did my own LCM implementation which makes more sense and finishes in a reasonable time

def lcm_better(a, b, c):

    def getPrimeFactors(x):
        val = x
        factors = {}

        for factor in range(2, val):
            if val % factor == 0:
                factors[factor] = 0
                while val % factor == 0:
                    val /= factor
                    factors[factor] += 1

            if val == 1:
                break

        if val != 1:
            factors[val] = 1

        return factors

    primeA = getPrimeFactors(a)
    primeB = getPrimeFactors(b)
    primeC = getPrimeFactors(c)

    print "primes of", a,  primeA
    print "primes of", b, primeB
    print "primes of", c, primeC

    lcm_primes = {}
    for primeList in [primeA, primeB, primeC]:
        for prime in primeList.keys():
            if prime not in lcm_primes or lcm_primes[prime] < primeList[prime]:
                lcm_primes[prime] = primeList[prime]

    print "merged primes", lcm_primes

    lcm_accum = 1
    for prime in lcm_primes.keys():
        lcm_accum *= int(math.pow(prime, lcm_primes[prime]))

    return lcm_accum

print lcm_better(x_period, y_period, z_period)
    