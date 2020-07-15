from itertools import permutations
from _lib import getListOfNumbersForDay, IntCodeProgram

myInput = getListOfNumbersForDay(7)

# Test all orders and keep max
bestOrder = None
bestLast = 0
for order in  permutations(range(5)):
    programOutput = 0
    for givenValue in order:
        memory = myInput[:]  # make copy
        outputs = []
        computer = IntCodeProgram(
            myInput,
            inputs=[givenValue, programOutput],
            outputs=outputs,
            verbose=True
        )
        computer.run()
        programOutput = outputs[-1]

    lastOutput = programOutput
    if lastOutput > bestLast:
        bestOrder = order
        bestLast = lastOutput

print "best"
print bestOrder
print bestLast