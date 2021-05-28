import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This file takes in multiple data files to plot on one graph
"""

filenames = ["./Input/data6.txt", "./Input/data1.txt"]


def loadData(tests, samples):
    data = [[] for x in range(len(filenames))]
    for i, fn in enumerate(filenames):
        with open(fn) as f:
            lines = f.readlines()  # Reads every line into a list
            lowR = 0
            for r in range(tests):  # For each experiment...
                data[i].append([float(lines[x]) for x in range(lowR, lowR + samples)])
                lowR += (samples + 1)  # Offset due to file format (avoids blank line and label)
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

    # data2 = data[0]
    # data3 = data[1]
    # data4 = data[2]
    # data5 = data[3]
    # order = []
    # for v in avg_data:
    #     order.append(v[5] - 1)

    # data2n = [data2[i] for i in order]
    # data3n = [data3[i] for i in order]
    # data4n = [data4[i] for i in order]
    # data5n = [data5[i] for i in order]

    # data = []
    # order = []
    # for li in all_data:
    # order.append(li[0])
    # data.append(li[3])

    # Plot data:
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    fig = plt.figure()  # Creates a figure from the plot
    # fig.suptitle('ED-Fitness on SIR(S) with Point Packing', fontsize=12, fontweight='bold')

    ax = fig.add_subplot(111)

    # axs = []
    # for i in range(len(filenames)):
    #     axs.append(fig.add_subplot(int(str(22) + str(i+1))))

    # Add information to said subplot:
    end = len(filenames) * 8+1
    xs = [x for x in range(1, end, len(filenames))]
    xs1 = [x for x in range(2, end, len(filenames))]
    # xs2 = [x for x in range(3, end, len(filenames))]
    # xs3 = [x for x in range(4, end, len(filenames))]
    # xs4 = [x for x in range(5, end, len(filenames))]
    xls = range(1,ps_count+1)
    locs = [x for x in range(int(len(filenames)/2)+1, end, len(filenames))]

    ys0, ys1, ys2, ys3, ys4, ys5, ys6 = [], [], [], [], [], [], []
    yse0, yse1, yse2, yse3, yse4, yse5, yse6 = [], [], [], [], [], [], []
    for v in avg_data:
        # xls.append(v[5])
        ys0.append(v[0][0])
        yse0.append(v[0][1])
        ys1.append(v[1][0])
        yse1.append(v[1][1])
        # yse2.append(v[2][1])
        # ys2.append(v[2][0])
        # yse3.append(v[3][1])
        # ys3.append(v[3][0])
        # yse4.append(v[4][1])
        # ys4.append(v[4][0])

    size = 8
    ax.set_title("Epidemic Length with Single Community by Size",size=10)

    col1 = (0,0,1)
    col2 = (1,0,0)
    # col2p = "orange"
    # col3 = "blue"
    # col3p = "green"
    ax.scatter(xs1, ys1, size, label="512 Nodes",color=col2)
    ax.errorbar(xs1, ys1, yerr=yse1, fmt="|", color=col2)
    ax.scatter(xs, ys0, size, label="128 Nodes",color=col1)
    ax.errorbar(xs, ys0, yerr=yse0, fmt="|", color=col1)

    # ax.scatter(xs2, ys2, size, label="3",color=col2p)
    # ax.errorbar(xs2, ys2, yerr=yse2, fmt="|", color=col2p)
    # ax.scatter(xs3, ys3, size, label="4",color=col3)
    # ax.errorbar(xs3, ys3, yerr=yse3, fmt="|", color=col3)
    # ax.scatter(xs4, ys4, size, label="5", color=col3p)
    # ax.errorbar(xs4, ys4, yerr=yse4, fmt="|", color=col3p)
    plt.xticks(locs, xls)
    plt.xlabel("Parameter Setting")
    ax.legend(fontsize=7, frameon=False, loc="center right")

    # axs[0].set_title("SIR", size=10)
    # axs[1].set_title("SIRS 10", size=10)
    # axs[2].set_title("SIRS 8", size=10)
    # axs[3].set_title("SIRS 6", size=10)
    #
    # axs[0].boxplot(data2n, 0, "")
    # axs[1].boxplot(data5n, 0, "")
    # axs[2].boxplot(data4n, 0, "")
    # axs[3].boxplot(data3n, 0, "")
    #
    # for i, a in enumerate(axs):
    #     a.set_xticks(locs)
    #     a.set_xticklabels(labels)
    #     for i in range(4,29,4):
    #         a.axvline(x=i+0.5,ymin=0,ymax=1,linewidth=1)

    for i in range(len(filenames), end-1, len(filenames)):
        ax.axvline(x=i + 0.5, ymin=0, ymax=1, linewidth=1)

    plt.tight_layout(0.5, 0.25, 0.25)
    fig.savefig('./Output/AvF.png')

    f = open('./Output/AvF_table' + '.txt', 'w')
    for p in range(ps_count):
        f.write(str(p + 1) + "\t")
        for e in range(len(filenames)):
            l = data[e][p]
            mean = float(np.mean(l))
            std = float(np.std(l, ddof=0))
            std = round(std, 4)
            diff = 1.96 * std / math.sqrt(30)
            diff = round(diff, 4)
            mean = round(mean, 4)
            m = round(max(l), 4)
            f.write(str(mean) + "\t" + str(mean) + '\u00B1' + str(diff) + '\t' + str(std) + '\t' + str(m) + "\t")
        f.write("\n")


# Command line calls
main(int(sys.argv[1]), int(sys.argv[2]))

# Run line:
# Num PSs
# Samples per PS
# python make_Combo.py 29 30
