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
    # >> BUT IT DOES NOT COUNT IF THERE ARE THREE <<
    # + always-increasing digits
    numberStr = str(number)
    has_adjacent_digits = False
    always_increasing = True

    # If we are in a group of >2 adjacent,
    # blacklist that number so that we don't check for adjacency
    blacklisted_number = None

    for d in range(1, len(numberStr)):
        cur = numberStr[d]
        prev = numberStr[d-1]

        if cur != blacklisted_number:
            # clear the blacklist once we're out of the adjacent zone
            blacklisted_number = None

        if cur != blacklisted_number and  prev == cur:
            # OK WE HAVE 2 ADJACENT
            # LET'S CHECK THE THIRD IS NOT ADJACENT
            # (there's a special case for the last digit)
            if d == len(numberStr) - 1 or cur != numberStr[d+1]:
                has_adjacent_digits = True
            else:
                blacklisted_number = cur

        if prev > cur:
            always_increasing = False
            break
    return has_adjacent_digits and always_increasing

counter = 0
for n in range(RANGE[0], RANGE[1]):
    # condition 1 is always true if condition 2 is true
    if condition2(n) and condition3_4(n):
        counter += 1

print counter

# 2779 too high (obv's because that's part 1 answer2779)