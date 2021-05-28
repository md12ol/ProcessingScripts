import sys

"""
This script takes in allData.txt which has all data from all profiles from all parameter settings.
To make the table used to create 
"""


def load_data(filename, tests, profiles, samples):
    # This is just a nifty python thing that lets us avoid exceptions
    with open(filename) as f:
        lines = f.readlines()  # Reads every line into a list
        data = [[] for i in range(tests)]
        low_r = 1  # Offset to avoid the label
        for t in range(tests):  # For each experiment...
            for p in range(profiles):  # For each profile...
                # Grab data from the lines but cast it into a float
                data[t].append([float(lines[x]) for x in range(low_r, low_r + samples)])  # Creates an array of arrays
                low_r += (samples + 2)  # Offset due to file format (avoids blank line and label)
        return data  # Returns as a 3d array (experiment num)(profile num)(sample num)


def main(fName, tests, profiles, samples):
    # data[testNum][profileNum] is a list of the 30 best fitnesses from the runs
    data = load_data(fName, int(tests), int(profiles), int(samples))
    # bestFitness[testNum][profileNum] is the best fitness found for that (test, profile) combo
    bestFitness = [[0 for j in range(int(profiles))] for i in range(int(tests))]
    for t in range(int(tests)):
        for p in range(int(profiles)):
            bestFitness[t][p] = min(data[t][p])

    # rank[testNum][profileNum] is the rank that PS(test) has compared to
    #  the other PSings on that particular profile
    rank = [[0 for j in range(int(profiles))] for i in range(int(tests))]
    for p in range(int(profiles)):
        minF = 1000
        nextMinF = 1000
        curRank = 1
        assigned = 0
        # findMin
        for t in range(int(tests)):
            if bestFitness[t][p] < minF:
                minF = bestFitness[t][p]

        # assign rank
        for t in range(int(tests)):
            if bestFitness[t][p] == minF:
                rank[t][p] = curRank
                assigned += 1
        curRank += 1

        while (assigned < 29):
            # Get the next min
            for t in range(int(tests)):
                if bestFitness[t][p] < nextMinF and bestFitness[t][p] > minF:
                    nextMinF = bestFitness[t][p]

            # Assign rank
            for t in range(int(tests)):
                if bestFitness[t][p] == nextMinF:
                    rank[t][p] = curRank
                    assigned += 1
            curRank += 1

            minF = nextMinF
            nextMinF = 1000

    f = open('RankTable.txt', 'w')
    for t in range(int(tests)):
        f.write(str(t + 1) + '\t')
        for p in range(int(profiles)):
            f.write(str(rank[t][p]) + '\t')
        f.write('\n')
    f.close()


# Command line calls
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# Run line:
# Data File
# Num Experiments (Tests)
# Num Profiles
# Samples per Experiment+Profile Pair
# python make_rank.py allData.txt 29 9 30
