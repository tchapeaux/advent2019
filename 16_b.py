with open('inputs/input16.txt') as f:
    firstInput = list(f.read().strip())


def patternAtStep(i):
    if i not in PATTERN_STEPS:
        PATTERN_STEPS[i] = (i + 1) * (0,) + (i + 1) * (1,) + (i + 1) * (0,) + (i + 1) * (-1,)
    return PATTERN_STEPS[i]

PATTERN_STEPS = {}

def getNextPhase(phaseInput):
    output = []
    for i in range(len(phaseInput)):
        pattern = patternAtStep(i)
        currentSum = 0
        for idx, elem in enumerate(phaseInput):
            phaseValue = pattern[(idx + 1) % len(pattern)]
            currentSum += phaseValue * elem
            # print "+", phaseValue, "*", elem
        # print "=", currentSum
        output.append((abs(currentSum) % 10))

    # print "new phase is", output
    return output

# Examples from the instruction
# [1,2,3,4,5,6,7,8]
# list("80871224585914546619083218645595")
# list("19617804207202209144916044189917")
# list("69317163492948606335995924319873")

print len(firstInput * 10000)
print "5979187"

currentPhase = firstInput * 100
currentPhase = [int(x) for x in currentPhase]

print "Phase 000"
for i in range(100):
    newPhase = getNextPhase(currentPhase)
    print "Phase", str(i+1).zfill(3), ":", newPhase[:8]
    currentPhase = newPhase

print "".join([str(c) for c in currentPhase][:8])