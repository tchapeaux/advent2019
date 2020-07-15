from itertools import permutations
from _lib import getListOfNumbersForDay, IntCodeProgram

myInput = getListOfNumbersForDay(7)

# Test all orders and keep max
bestOrder = None
bestLast = 0
for order in  permutations(range(5, 10)):
    computers = []
    for givenValue in order:
        memory = myInput[:]  # make copy
        computers.append(IntCodeProgram(
            memory,
            inputs=[givenValue],
        ))

    currentComputerIdx = 0
    lastOutput = 0
    while not all([c._halted for c in computers]):
        currentComputerIdx = (currentComputerIdx + 1) % len(computers)
        computer = computers[currentComputerIdx]

        computer.inputs.append(lastOutput)
        computer._waitingForInput = False

        computer.run()

        lastOutput = computer.outputs.pop()

    if lastOutput > bestLast:
        bestLast = lastOutput
        bestOrder = order

print "best"
print bestOrder
print bestLast