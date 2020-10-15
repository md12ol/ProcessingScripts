import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This script makes a boxplot of the fitness (numerical) vs parameter setting
"""


def loadData(fName, tests, samples):
    with open(fName) as f:
        lines = f.readlines()  # Reads every line into a list
        data = []
        lowR = 0  # Offset to avoid the label
        for r in range(tests):  # For each experiment...
            # Grab data from the lines but cast it into a float
            data.append([float(lines[x]) for x in range(lowR, lowR + samples)])  # Creates an array of arrays
            lowR += (samples + 1)  # Offset due to file format (avoids blank
            # line and label)
        return data  # Returns as a 2d array


def main(exp_label, ps_count, samps):
    input_file = "./Input/data" + exp_label + ".txt"
    data = loadData(input_file, ps_count, samps)
    sums = [(i + 1, sum(data[i])) for i in range(len(data))]

    # sums = sorted(sums,key=itemgetter(1))

    # data[1] = []
    # data[2] = []
    # data[5][:] = (value for value in data[5] if value != 0)

    order = []
    for v in sums:
        order.append(v[0])

    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    locs = range(1, 9)
    order = [str(o) for o in order]
    # fig = plt.figure(figsize=(4.8, 4.8))

    # axs = []
    # for i in range(3):
    #     axs.append(fig.add_subplot(int(str(31) + str(i + 1))))

    # for i, a in enumerate(axs):
    #     s, e = i * 30, (i + 1) * 30
    #     a.boxplot(data[s:e], 0, "")
    #     a.set_xticks(locs)
    #     a.set_xticklabels(order[s:e])
    #     for i in range(2, 31, 2):
    #         a.axvline(x=i + 0.5, ymin=0, ymax=1, linewidth=1)

    ax.boxplot(data,0, "")

    plt.tight_layout(0.5, 0.5, 0)

    fig.savefig('./Output/boxplot' + str(exp_label) + '.png')

    f = open('./Output/table' + str(exp_label) + '.txt', 'w')
    for r in range(int(ps_count)):
        if data[r]!=[]:
            mean = float(np.mean(data[r]))
            std = float(np.std(data[r], ddof=0))
            std = round(std, 4)  # Population standard deviation
            diff = 1.96 * std / math.sqrt(30)  # 95% CI
            diff = round(diff, 4)
            mean = round(mean, 4)
            m = round(max(data[r]), 4)
        else:
            mean = 0
            std = 0
            diff = 0
            m = 0

        f.write(str(r + 1) + '\t' + str(mean) + '\t' + str(mean) + '\u00B1' + str(diff) + '\t' + str(std) + '\t' +
                str(m) + '\n')
    f.close()


# Command line calls
main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

# Run line:
# Experiment Label
# Number of PSs
# Samples per PS
# python boxplot.py 1 29 30
