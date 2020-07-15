from _lib import getListOfNumbersForDay, IntCodeProgram

myProgram = getListOfNumbersForDay(13)
myProgram[0] = 2  # free quarters woo!
computer = IntCodeProgram(myProgram, inputs=[], outputs=[])

grid = {}

def parseTileInstructions(instr):
    for idx in range(0, len(instr), 3):
        coords = (instr[idx], instr[idx + 1])
        tileId = int(instr[idx + 2])
        grid[coords] = tileId

def showGrid():
    max_x = max([c[0] for c in grid.keys()])
    max_y = max([c[1] for c in grid.keys()])

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            tileId = grid[(x, y)] if (x, y) in grid else None
            if tileId == 0 or not tileId:
                print ' ',
            elif tileId == 1:
                print '#',
            elif tileId == 2:
                print 'B',
            elif tileId == 3:
                print '=',
            elif tileId == 4:
                print 'O',
        print ""
    print "SCORE", grid[(-1, 0)]

while not computer._halted:
    computer.run()

    tileInstructions = computer.outputs
    parseTileInstructions(tileInstructions)
    del computer.outputs[:]

    # showGrid()

    # Super AI:
    # If ball is right of paddle, go right
    # If ball is left of paddle, go left
    # If ball is above paddle, don't move

    ball = [coord for (coord, tileType) in grid.items() if tileType == 4][0]
    paddle = [coord for (coord, tileType) in grid.items() if tileType == 3][0]

    if paddle[0] < ball[0]:
        computer.inputs.append(1)
    elif paddle[0] > ball[0]:
        computer.inputs.append(-1)
    else:
        computer.inputs.append(0)

showGrid()