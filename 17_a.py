from _lib import getListOfNumbersForDay, IntCodeProgram

myProgram = getListOfNumbersForDay(17)
computer = IntCodeProgram(myProgram, inputs=[], outputs=[])


computer.run()

initialState = [chr(c) for c in computer.outputs]

grid = {}

# Parse array of ASCII into a grid
currentRow = 0
currentRowOffset = 0
for idx, char in enumerate(initialState):
    if char == '\n':
        currentRow += 1
        currentRowOffset = idx + 1
    else:
        rowIdx = idx - currentRowOffset
        print currentRow, rowIdx
        grid[(currentRow, rowIdx)] = char

min_x = min([coord[0] for coord in grid.keys()])
max_x = max([coord[0] for coord in grid.keys()])
min_y = min([coord[1] for coord in grid.keys()])
max_y = max([coord[1] for coord in grid.keys()])

def showGrid():
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print grid[(x, y)],
        print ""

showGrid()

intersections = []

# Find intersections
# An intersection is a scaffolding '#'
# where the 4 neighbors cells (U, D, L, R)
# - Are within bounds
# - Contains a scaffolding ('#')
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if grid[(x, y)] == '#':
            isIntersection = True
            for (dX, dY) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if (x + dX, y + dY) not in grid or grid[(x + dX, y + dY)] != '#':
                    isIntersection = False

            if isIntersection:
                intersections.append((x, y))

print intersections

print sum([i[0] * i[1] for i in intersections])
