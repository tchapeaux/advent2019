from _lib import getListOfNumbersForDay, IntCodeProgram

myInput = getListOfNumbersForDay(5)

outputs = []

computer = IntCodeProgram(myInput, inputs=[1], outputs=outputs, verbose=True)
computer.run()

print outputs