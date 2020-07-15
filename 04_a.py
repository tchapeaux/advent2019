## ADVENT OF CODE 2019
# Day 4 - Part I
# Basically find out how many numbers in a range respect some conditions

RANGE = (108457, 562041)

def condition1(number):
    # 6-digits number
    return 99999 < number < 1000000

def condition2(number):
    # in the range of my input
    # my input is hardcoded in this case
    return RANGE[0] < number < RANGE[1]

def condition3_4(number):
    # two adjacents digits are the same
    # + always-increasing digits
    numberStr = str(number)
    has_adjacent_digits = False
    always_increasing = True
    for d in range(1, len(numberStr)):
        cur = numberStr[d]
        prev = numberStr[d-1]
        if prev == cur:
            has_adjacent_digits = True
        if prev > cur:
            always_increasing = False
    return has_adjacent_digits and always_increasing

counter = 0
for n in range(RANGE[0], RANGE[1]):
    # condition 1 is always true if condition 2 is true
    if condition2(n) and condition3_4(n):
        counter += 1

print counter