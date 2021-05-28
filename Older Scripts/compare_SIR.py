import re
import sys

"""
Takes best.lint data from one experiment and places it in data[exp num].txt.
"""


def loadData(fName):
    data = []
    with open(fName) as f:  # This is just a nifty python thing that lets us avoid exceptions
        lines = f.readlines()  # Reads every line into a list
        for line in lines:
            if line.__contains__(str("fitnessPM")):
                data.append(float(re.findall("\d+\.\d+", line)[0]))
    data.sort()
    data.reverse()
    return data  # Returns as a 3d array (experiment num)(profile num)(sample num)


def main(exp_num, prof_count, samps):
    out = open('./Output/data' + str(exp_num) + '.txt', 'w')
    for t in range(int(prof_count)):  # for each Profile
        data = loadData("./Input/" + str(exp_num) + "/P" + str(t + 1) +
                        "/best.lint")
        assert len(data) == samps
        for d in data:
            out.write(str(d) + "\n")
        out.write("\n")  # separator
    out.close()


# Command line call
main(sys.argv[1], sys.argv[2], int(sys.argv[3]))

# Run line:
# Experiment Number
# Num of Profiles
# Samples per PS
# python make_data.py 1 29 30
