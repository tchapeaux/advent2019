from _lib import getListOfNumbersForDay, IntCodeProgram

myProgram = getListOfNumbersForDay(13)

# print myProgram

computer = IntCodeProgram(myProgram, inputs=[], outputs=[])

computer.run()

tileInstructions = computer.outputs

grid = {}

for idx in range(0, len(tileInstructions), 3):
    coords = (tileInstructions[idx], tileInstructions[idx + 1])
    tileId = int(tileInstructions[idx + 2])
    grid[coords] = tileId

print len(grid.keys()), "tiles"
print len([t for t in grid.keys() if grid[t] == 2]), "blocks"