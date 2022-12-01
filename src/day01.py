# Day 1: Calorie Counting

# read calories from text field into a list of integers
def load_cals(cals_file):
    sumcals = 0
    maxcals = 0

    # Part 1
    with open(cals_file, "r") as cfile:
        for line in cfile:
            if line == "\n":  # blank line
                maxcals = max(sumcals, maxcals)
                sumcals = 0
            else:
                sumcals += int(line.strip())

    return maxcals


# Part 2
def top_3_cals(cals_file):
    cals = []
    sumcals = 0
    with open(cals_file, "r") as cfile:
        for line in cfile:
            if line == "\n":  # need a blank line at end of test file
                cals.append(sumcals)
                sumcals = 0
            else:
                sumcals += int(line.strip())
    # need three highest values in list
    cals.sort()
    return cals[-1] + cals[-2] + cals[-3]
