from _lib import getListOfNumbersForDay, IntCodeProgram

myInput = getListOfNumbersForDay(2)

def runProgram(noun, verb):
    memory = myInput[:]
    memory[1] = noun
    memory[2] = verb

    computer = IntCodeProgram(memory)
    computer.run()
    return computer.memory[0]

assert runProgram(12, 2) == 5866714

# Brute force that poop
for noun in range(100):
    for verb in range(100):
        if runProgram(noun, verb) == 19690720:
            print(noun, verb, noun * 100 + verb)