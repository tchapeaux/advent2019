from itertools import permutations
from _lib import getListOfNumbersForDay, IntCodeProgram

import pdb

memory = getListOfNumbersForDay(11)

visitedPanels = set()
whitePanels = set()  # non-white panels are always black

currentPosition = (0, 0)

directions = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}
currentDirection = directions['UP']

def updateDirection(currentDirection, directionCmd):
    if directionCmd == 0:
        return {
            directions['UP']: directions['LEFT'],
            directions['LEFT']: directions['DOWN'],
            directions['DOWN']: directions['RIGHT'],
            directions['RIGHT']: directions['UP'],
        }[currentDirection]
    elif directionCmd == 1:
        return {
            directions['UP']: directions['RIGHT'],
            directions['RIGHT']: directions['DOWN'],
            directions['DOWN']: directions['LEFT'],
            directions['LEFT']: directions['UP'],
        }[currentDirection]
    else:
        raise Exception('Unknown direction cmd', directionCmd)

def updatePosition(currentPosition, currentDirection):
    return (
        currentPosition[0] + currentDirection[0],
        currentPosition[1] + currentDirection[1]
    )

def showDirection(dir):
    if dir == directions['UP']:
        return '^'
    if dir == directions['DOWN']:
        return 'v'
    if dir == directions['LEFT']:
        return '<'
    if dir == directions['RIGHT']:
        return '>'

inputs = []
outputs = []

computer = IntCodeProgram(memory, inputs=inputs, outputs=outputs)

while True:
    print showDirection(currentDirection), currentPosition, computer._currentStepCount

    if computer._waitingForInput and len(inputs) == 0:
        currentPanelColor = 1 if currentPosition in whitePanels else 0
        inputs.append(currentPanelColor)
    print '_i', inputs

    # pdb.set_trace()

    computer.run()

    if computer._halted:
        break

    assert computer._waitingForInput


    if len(outputs) == 2:
        # print '_o', outputs
        directionCmd = outputs.pop()
        paintCmd = outputs.pop()

        if paintCmd == 1:
            whitePanels.add(currentPosition)
        elif paintCmd == 0:
            whitePanels.remove(currentPosition)

        visitedPanels.add(currentPosition)

        currentDirection = updateDirection(currentDirection, directionCmd)
        currentPosition = updatePosition(currentPosition, currentDirection)
    else:
        assert len(outputs) == 0

print computer.outputs
print len(visitedPanels)

min_x = min([p[0] for p in whitePanels])
max_x = max([p[0] for p in whitePanels])
min_y = min([p[1] for p in whitePanels])
max_y = max([p[1] for p in whitePanels])

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        print "#" if (x, y) in whitePanels else ".",
    print ""