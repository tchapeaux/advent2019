import math

from _lib import getLinesForDay 

myInput = getLinesForDay(1)

def getFuel(mass):
    return int(math.floor(mass / 3)) - 2

def getTotalFuel(mass):
    fuelAccum = 0

    newQuantity = getFuel(mass)
    while newQuantity > 0:
        fuelAccum += newQuantity
        newQuantity = getFuel(newQuantity)

    return fuelAccum

totalFuel = 0
for mass in myInput:
    totalFuel += getTotalFuel(int(mass))

print(totalFuel)

# 5115729 x too low