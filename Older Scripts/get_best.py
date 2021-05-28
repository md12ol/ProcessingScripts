import sys

"""
Creates PointPackingTable data from CEC 2019 (others)
"""


def loadData(fName, tests, profiles, samples):
    # This is just a nifty python thing that lets us avoid exceptions
    with open(fName) as f:
        lines = f.readlines()  # Reads every line into a list
        data = [[] for i in range(tests)]
        lowR = 1  # Offset to avoid the label
        for t in range(tests):  # For each experiment...
            for p in range(profiles):  # For each profile...
                # Grab data from the lines but cast it into a float
                data[t].append([float(lines[x]) for x in range(lowR, lowR + samples)])  # Creates an array of arrays
                lowR += (samples + 2)  # Offset due to file format (avoids
                # blank line and label)
        return data  # Returns as a 3d array (experiment num)(profile num)(sample num)


def main(fName, tests, profiles, samples):
    data = loadData(fName, int(tests), int(profiles), int(samples))
    f = open('PointPackingTable.txt', 'w')
    for t in range(int(tests)):
        f.write(str(t + 1) + '\t')
        for p in range(int(profiles)):
            f.write(str(min(data[t][p])) + '\t')
        f.write('\n')
    f.close()


# Command line calls
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# Run line:
# Data File
# Num Experiments (Tests)
# Num Profiles
# Samples per Experiment+Profile Pair
# python get_best.py allData.txt 29 9 30
