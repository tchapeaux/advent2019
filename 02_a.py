from _lib import getListOfNumbersForDay, IntCodeProgram

myInput = getListOfNumbersForDay(2)

# Do the replacement in the instructions
myInput[1] = 12
myInput[2] = 2

computer = IntCodeProgram(myInput, verbose=True)
computer.run()

print computer.memory[0]