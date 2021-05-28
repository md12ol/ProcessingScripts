import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This file takes in data1-9.txt and creates a 3by3 rep
"""

filenames = ["./Input/data1.txt", "./Input/data2.txt", "./Input/data3.txt", "./Input/data4.txt", "./Input/data5.txt",
             "./Input/data6.txt", "./Input/data7.txt", "./Input/data8.txt", "./Input/data9.txt"]


def loadData(tests, samples):
    data = [[] for x in range(len(filenames))]
    for i, fn in enumerate(filenames):
        with open(fn) as f:
            lines = f.readlines()  # Reads every line into a list
            lowR = 1
            for r in range(tests):  # For each experiment...
                data[i].append([float(lines[x]) for x in range(lowR, lowR + samples)])
                lowR += (samples + 2)  # Offset due to file format (avoids blank line and label)
    return data  # (exp, PS) pairs --> 30 results


def main(ps_count, samps):
    data = loadData(ps_count, samps)
    avg_data = [[] for x in range(ps_count)]  # (PS, exp) --> avg for PS on exp

    for ps in range(ps_count):
        for exp in range(len(filenames)):
            std = float(np.std(data[exp][ps], ddof=0))
            std = round(std, 4)  # Population standard deviation
            diff = 1.96 * std / math.sqrt(30)  # 95% CI
            diff = round(diff, 4)
            avg_data[ps].append((np.mean(data[exp][ps]), diff))  # 0, 1 --> mean, diff

    for ps in range(ps_count):
        sum = 0
        for exp in range(len(filenames)):
            sum += avg_data[ps][exp][0]
        avg_data[ps].append(sum)  # 4 (sum of 0(0)-3(0))
        avg_data[ps].append(ps + 1)  # 5 (ps num)

    '''
    avg_data[ps][exp 0-3][0-1] --> (ps, exp, [0, 1]) --> mean, diff of samps from (exp, ps)
    avg_data[ps][4] --> sum of avg_data[ps][0:3][0]
    avg_data[ps][5] --> ps (after jumble ps will be kept)
    '''

    # avg_data = sorted(avg_data, key=itemgetter(4))

    order = []
    for v in avg_data:
        order.append(v[len(filenames) + 1])

    # Plot data:
    plt.rc('xtick', labelsize=7)
    plt.rc('ytick', labelsize=7)

    locs = [1]
    for i in range(4, 25, 5):
        locs.append(i)
    labels = ["1", "2-6", "7-11", "12-16", "17-21", "22-26"]
    fig = plt.figure()  # Creates a figure from the plot

    axs = []
    for i in range(len(filenames)):
        axs.append(fig.add_subplot(int(str(33) + str(i + 1))))

    for i, a in enumerate(axs):
        a.set_title("Profile " + str(i + 1), fontsize=8)
        a.boxplot(data[i], 0, "", labels=order)
        a.set_xticks(locs)
        a.set_xticklabels(labels)
        for i in range(1, 22, 5):
            a.axvline(x=i + 0.55, ymin=0, ymax=1, linewidth=1.25)

    plt.tight_layout(0.5, 0.5, 0.5)

    # plt.tight_layout()
    fig.savefig('./Output/PPall.png')

    for i in range(len(filenames)):
        f = open('./Output/PP' + str(i + 1) + '_table.txt', 'w')
        for r in range(int(ps_count)):
            mean = float(np.mean(data[i][r]))
            std = float(np.std(data[i][r], ddof=0))
            std = round(std, 4)  # Population standard deviation
            diff = 1.96 * std / math.sqrt(30)  # 95% CI
            diff = round(diff, 4)
            mean = round(mean, 4)
            m = round(min(data[i][r]), 4)
            f.write(str(r + 1) + '\t' + str(mean) + '\t' + str(mean) + '\u00B1' + str(diff) + '\t' + str(std) + '\t' +
                    str(m) + '\n')
        f.close()


# Command line calls
main(int(sys.argv[1]), int(sys.argv[2]))

# Run line:
# Num PSs
# Samples per PS
# python make_Combo.py 29 30
