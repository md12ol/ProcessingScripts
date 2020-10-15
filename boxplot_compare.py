import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This script makes a boxplot of the fitness (numerical) vs parameter setting 
of two experiments on one graph
"""


def loadData(fName, tests, samples):
    with open(fName) as f:
        lines = f.readlines()  # Reads every line into a list
        data = []
        lowR = 0  # Offset to avoid the label
        for r in range(tests):  # For each experiment...
            # Grab data from the lines but cast it into a float
            data.append([float(lines[x]) for x in range(lowR,
                                                        lowR + samples)])  # Creates an array of arrays
            lowR += (samples + 1)  # Offset due to file format (avoids blank
            # line and label)
        return data  # Returns as a 2d array


def out_table(exp_label, ps_count, data):
    f = open('./Output/table' + str(exp_label) + '.txt', 'w')
    for r in range(int(ps_count)):
        if data[r] != []:
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

        f.write(
            str(r + 1) + '\t' + str(mean) + '\t' + str(mean) + '\u00B1' + str(
                diff) + '\t' + str(std) + '\t' +
            str(m) + '\n')
    f.close()


def main(exp_label1, exp_label2, exp_num, ps_count, samps):
    input_file1 = "./Input/data" + exp_label1 + str(exp_num) +  ".txt"
    input_file2 = "./Input/data" + exp_label2 + str(exp_num) + ".txt"
    data1 = loadData(input_file1, ps_count, samps)
    data2 = loadData(input_file2, ps_count, samps)
    # sums = [(i + 1, sum(data[i])) for i in range(len(data))]

    # sums = sorted(sums,key=itemgetter(1))

    # data[1] = []
    # data[2] = []
    # data[5][:] = (value for value in data[5] if value != 0)

    # order = []
    # for v in sums:
    #     order.append(v[0])

    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.suptitle("SIR v. SIIR on Profile " + str(exp_num))

    locs = [i + 0.5 for i in range(1, 17, 2)]
    order = [str(i) for i in range(1,9)]
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

    combo_data = []
    for i in range(ps_count):
        combo_data.append(data1[i])
        combo_data.append(data2[i])

    ax.boxplot(combo_data)
    ax.set_xlabel("Experiment")
    ax.set_ylabel("PM-Fitness")

    for i in range(ps_count * 2):
        ax.set_xticks(locs)
        ax.set_xticklabels(order)

    for i in range(1,ps_count+1):
        ax.axvline(x=i*2 + 0.5, ymin=0, ymax=1, linewidth=1)

    plt.tight_layout(1.5)

    fig.savefig('./Output/boxplot' + str(exp_label1) + str(exp_num) + '.png')

    out_table(exp_label1 + str(exp_num), ps_count, data1)
    out_table(exp_label2 + str(exp_num), ps_count, data2)


# Command line calls
main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),
     int(sys.argv[5]))

# Run line:
# Experiment Label 1
# Experiment Label 2
# Experiment Number
# Num of PSs
# Samples per PS
# python boxplot_compare.py ./PS1/ ./PS2/ 1 29 30
