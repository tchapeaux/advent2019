from itertools import permutations
from _lib import getListOfNumbersForDay, IntCodeProgram

memory = getListOfNumbersForDay(9)

computer = IntCodeProgram(memory, inputs=[1], verbose=True)
computer.run()
assert computer._halted

print computer.outputs

# 203 : too low