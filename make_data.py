import re
import sys

"""
Takes best.lint data from one experiment and places it in data[exp num].txt.
"""

inp = "./Input/"
exp_str = "SIR"
prof_count = 9
samps = 30

def loadData(fName):
    data = []
    with open(fName) as f:  # This is just a nifty python thing that lets us avoid exceptions
        lines = f.readlines()  # Reads every line into a list
        for line in lines:
            if line.__contains__(str("fitness")):
                data.append(float(re.findall("\d+\.\d+", line)[0]))
    data.sort()
    data.reverse()
    return data


def main(exp_num):
    out = open('./Output/data' + str(exp_str) + str(exp_num) + '.txt', 'w')
    for prof in range(prof_count):  # for each PS
        data = loadData(inp + exp_str + str(exp_num) + "/P" + str(prof + 1) + "/best.lint")
        assert len(data) == samps
        for d in data:
            out.write(str(d) + "\n")
        out.write("\n")  # separator
    out.close()


# Command line call
main(int(sys.argv[1]))

# Run line:
# Experiment Number
# Num of PSs
# Samples per PS
# python make_data.py 1 29 30
