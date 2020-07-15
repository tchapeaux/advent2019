import math

from _lib import getLinesForDay 

myInput = getLinesForDay(1)

def getFuel(mass):
    return int(math.floor(mass / 3)) - 2

assert getFuel(12) == 2
assert getFuel(14) == 2
assert getFuel(1969) == 654
assert getFuel(100756) == 33583

totalFuel = 0
for mass in myInput:
    totalFuel += getFuel(mass)

print totalFuel