def getLinesForDay(dayNbr):
    with open('inputs/input' + str(dayNbr).zfill(2) + ".txt") as f:
        return [line.strip() for line in  f.readlines() if len(line.strip()) > 0]

def getRawForDay(dayNbr):
    with open('inputs/input' + str(dayNbr).zfill(2) + ".txt") as f:
        return f.read()

def getCommaSeparatedLine(line):
    return [v for v in line.split(',')]

def getListOfNumbersForDay(dayNbr):
    lines = getLinesForDay(dayNbr)
    assert len(lines) == 1
    return [int(n) for n in lines[0].split(',')]

class Grid(object):
    def __init__(self):
        self._g = {}

    def get(self, x, y):
        if x not in self._g:
            return None
        if y not in self._g[x]:
            return None
        return self._g[x][y]

    def set(self, x, y, newVal):
        if x not in self._g:
            self._g[x] = {}
        self._g[x][y] = newVal

def manhattanDistance(x1, y1, x2, y2):
    # manhattan distance between (x1, y1) and (x2, y2)
    return abs(y2 - y1) + abs(x2 - x1)

class IntCodeProgram(object):
    def __init__(self, memory, inputs=[], outputs=[], verbose=False):
        self.memory = {}  # dict because we might have "holes" in memory
        for idx in range(len(memory)):
            self.memory[idx] = memory[idx]

        self.inputs = inputs
        self.outputs = outputs
        self.verbose = verbose

        self._started = False
        self._halted = False
        self._waitingForInput = False
        self._execPointer = 0
        self._relativeBase = 0
        self._currentStepCount = 0

    def run(self):
        self._started = True

        if self._waitingForInput:
            if len(self.inputs) == 0:
                raise Exception("Trying to start IntCode waiting for input with an empty inputs array")
            else:
                self._waitingForInput = False

        while not self._halted and not self._waitingForInput:
            self.step()

    def getMemory(self, address):
        if address in self.memory:
            return self.memory[address]
        # If address is not in memory: return 0
        return 0

    def setMemory(self, address, value):
        self.memory[address] = value

    def getParamValue(self, operand, paramMode):
        if paramMode == 0:
            # Position
            return self.getMemory(operand)
        elif paramMode == 1:
            # Immediate
            return operand
        elif paramMode == 2:
            # Relative
            return self.getMemory(self._relativeBase + operand)
        raise Exception('getParamValue: unknown param mode ' + str(paramMode))

    def step(self):
        instruction = self.getMemory(self._execPointer)

        self._currentStepCount += 1

        if self.verbose:
            print "==="
            print "Pointer", self._execPointer

            for idx in range(max(0, self._execPointer - 5), self._execPointer):
                print self.getMemory(idx), ",",
            print "[", instruction, "],",
            for idx in range(self._execPointer + 1, self._execPointer + 6):
                print self.getMemory(idx), ",",
            print ""


        # Parse instruction
        instruction = str(instruction).zfill(5)
        param3mode = int(instruction[0])
        param2mode = int(instruction[1])
        param1mode = int(instruction[2])
        opcode = int(instruction[3:])

        if opcode == 99:
            self._halted = True
        elif opcode == 1:
            # ADD
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            operand3 = self.getMemory(self._execPointer + 3)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)
            assert not param3mode == 1, "cannot write to immediate"
            write_location = operand3 if param3mode == 0 else self._relativeBase + operand3


            if self.verbose:
                print "[",write_location,"] = ", value1, "+", value2, "=", value1 + value2
            self.setMemory(write_location, value1 + value2)
            self._execPointer += 4
        elif opcode == 2:
            # MUL
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            operand3 = self.getMemory(self._execPointer + 3)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)
            assert not param3mode == 1, "cannot write to immediate"
            write_location = operand3 if param3mode == 0 else self._relativeBase + operand3

            if self.verbose:
                print "[",write_location,"] = ", value1, "*", value2, "=", value1 * value2
            self.setMemory(write_location, value1 * value2)
            self._execPointer += 4
        elif opcode == 3:
            # INP
            if len(self.inputs) == 0:
                self._waitingForInput = True
                self._currentStepCount -= 1  # Don't count this "missed" step
            else:
                operand1 = self.getMemory(self._execPointer + 1)
                _i = self.inputs.pop(0)
                assert not param1mode == 1, "cannot write to immediate"
                write_location = operand1 if param1mode == 0 else self._relativeBase + operand1

                if self.verbose:
                    print "[",write_location,"] = INPUT(", _i, ")"
                self.setMemory(write_location, _i)
                self._execPointer += 2
        elif opcode == 4:
            # OUT
            operand1 = self.getMemory(self._execPointer + 1)
            _o = self.getParamValue(operand1, param1mode)
            if self.verbose:
                print "OUTPUT:", _o
            self.outputs.append(_o)
            self._execPointer += 2
        elif opcode == 5:
            # JNZ (Jump-True)
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)

            if self.verbose:
                print "JMP TO", value2, "if", value1, "is true"
            self._execPointer = value2 if value1 != 0 else self._execPointer + 3
        elif opcode == 6:
            # JZE (Jump-False)
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)
            if self.verbose:
                print "JMP TO", value2, "if", value1, "is false"
            self._execPointer = value2 if value1 == 0 else self._execPointer + 3
        elif opcode == 7:
            # LT
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            operand3 = self.getMemory(self._execPointer + 3)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)
            assert not param3mode == 1, "cannot write to immediate"
            write_location = operand3 if param3mode == 0 else self._relativeBase + operand3

            if self.verbose:
                print "[",write_location,"] = " , value1, "<", value2
            self.setMemory(write_location, 1 if value1 < value2 else 0)
            self._execPointer += 4
        elif opcode == 8:
            # EQ
            operand1 = self.getMemory(self._execPointer + 1)
            operand2 = self.getMemory(self._execPointer + 2)
            operand3 = self.getMemory(self._execPointer + 3)
            value1 = self.getParamValue(operand1, param1mode)
            value2 = self.getParamValue(operand2, param2mode)
            assert not param3mode == 1, "cannot write to immediate"
            write_location = operand3 if param3mode == 0 else self._relativeBase + operand3

            if self.verbose:
                print "[",write_location,"] = " , value1, "==", value2
            self.setMemory(write_location, 1 if value1 == value2 else 0)
            self._execPointer += 4
        elif opcode == 9:
            # RBO (Relative Base Offset)
            operand1 = self.getMemory(self._execPointer + 1)
            value1 = self.getParamValue(operand1, param1mode)

            self._relativeBase += value1
            if self.verbose:
                print "RBO +=", value1, "=>", self._relativeBase
            self._execPointer += 2
        else:
            raise Exception("Unknown opcode " + str(opcode))
