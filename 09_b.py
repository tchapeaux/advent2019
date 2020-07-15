from itertools import permutations
from _lib import getListOfNumbersForDay, IntCodeProgram

memory = getListOfNumbersForDay(9)

computer = IntCodeProgram(memory, inputs=[2], verbose=False)
computer.run()
assert computer._halted

print computer.outputs

