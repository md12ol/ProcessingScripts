import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This file takes in data from the SIR and SIRS Point Packing data to compare results between re-susceptible period.  
Takes in data2.txt-data5.txt and outputs boxplotSIR(S).png and tableSIR(S).txt.
"""

filenames = ["./Input/dataM0X.txt", "./Input/dataM0A.txt",
             "./Input/dataM0B.txt", "./Input/dataM0C.txt"]
name = "M0V"
title = "Epidemic Length in Evolving Environment"

# filenames = ["./Input/dataM0X.txt", "./Input/dataM0As.txt",
#              "./Input/dataM0Bs.txt", "./Input/dataM0Cs.txt"]
# name = "M0Vs"
# title = "Epidemic Length in Static Environment"

# filenames = ["./Input/dataM1X.txt", "./Input/dataM1A.txt",
#              "./Input/dataM1B.txt", "./Input/dataM1C.txt"]
# name = "M1V"
# title = "Epidemic Spread in Evolving Environment"

# filenames = ["./Input/dataM1X.txt", "./Input/dataM1As.txt",
#              "./Input/dataM1Bs.txt", "./Input/dataM1Cs.txt"]
# name = "M1Vs"
# title = "Epidemic Spread in Static Environment"


def loadData(tests, samples):
    data = [[] for x in range(len(filenames))]
    for i, fn in enumerate(filenames):
        with open(fn) as f:
            lines = f.readlines()  # Reads every line into a list
            lowR = 0
            for r in range(tests):  # For each experiment...
                data[i].append(
                    [float(lines[x]) for x in range(lowR, lowR + samples)])
                lowR += (samples + 1)  # Offset due to file format (avoids blank line and label)
    return data  # (exp, PS) pairs --> 30 results


def main(ps_count, samps):
    data = loadData(ps_count, samps)
    avg_data = [[] for x in range(ps_count)]  # (PS, exp) --> avg for PS on exp

    # data[0][5][:] = (value for value in data[0][5] if value != 0)
    # data[1][5][:] = (value for value in data[1][5] if value != 0)
    # data[2][5][:] = (value for value in data[2][5] if value != 0)
    # data[3][5][:] = (value for value in data[3][5] if value != 0)

    for ps in range(ps_count):
        for exp in range(len(filenames)):
            std = float(np.std(data[exp][ps], ddof=0))
            std = round(std, 4)  # Population standard deviation
            diff = 1.96 * std / math.sqrt(30)  # 95% CI
            diff = round(diff, 4)
            avg_data[ps].append(
                (np.mean(data[exp][ps]), diff))  # 0, 1 --> mean, diff

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
    end = len(filenames) * 29 + 1
    xs = [x for x in range(1, end, len(filenames))]
    xs1 = [x for x in range(2, end, len(filenames))]
    xs2 = [x for x in range(3, end, len(filenames))]
    xs3 = [x for x in range(4, end, len(filenames))]
    # xs4 = [x for x in range(6, end, len(filenames))]
    # xs5 = [x for x in range(1, end, len(filenames))]
    xls = range(1, ps_count + 1)
    locs = [x + 0.5 for x in
            range(int(len(filenames) / 2), end, len(filenames))]

    ys0, ys1, ys2, ys3, ys4, ys5, ys6 = [], [], [], [], [], [], []
    yse0, yse1, yse2, yse3, yse4, yse5, yse6 = [], [], [], [], [], [], []
    for v in avg_data:
        # xls.append(v[5])
        ys0.append(v[0][0])
        yse0.append(v[0][1])
        ys1.append(v[1][0])
        yse1.append(v[1][1])
        ys2.append(v[2][0])
        yse2.append(v[2][1])
        ys3.append(v[3][0])
        yse3.append(v[3][1])
        # yse4.append(v[4][1])
        # ys4.append(v[4][0])
        # yse5.append(v[5][1])
        # ys5.append(v[5][0])

    size = 2
    ax.set_title(title, size=10)

    # ys0.__delitem__(1)
    # ys1.__delitem__(1)
    # ys2.__delitem__(1)
    # ys3.__delitem__(1)
    #
    # yse0.__delitem__(1)
    # yse1.__delitem__(1)
    # yse2.__delitem__(1)
    # yse3.__delitem__(1)
    #
    # ys0.__delitem__(1)
    # ys1.__delitem__(1)
    # ys2.__delitem__(1)
    # ys3.__delitem__(1)
    #
    # yse0.__delitem__(1)
    # yse1.__delitem__(1)
    # yse2.__delitem__(1)
    # yse3.__delitem__(1)
    #
    # xs.__delitem__(1)
    # xs1.__delitem__(1)
    # xs2.__delitem__(1)
    # xs3.__delitem__(1)
    #
    # xs.__delitem__(1)
    # xs1.__delitem__(1)
    # xs2.__delitem__(1)
    # xs3.__delitem__(1)

    col0 = "cyan"
    col1 = "red"
    col2 = "orange"
    col2p = "green"
    col3 = "blue"
    col3p = "orange"

    # ax.scatter(xs5, ys5, size, label="Original",color=col0)
    # ax.errorbar(xs5, ys5, yerr=yse5, fmt="|", color=col0)
    ax.scatter(xs, ys0, size, marker='*', label="No Vaccination", color=col1)
    ax.errorbar(xs, ys0, yerr=yse0, fmt="|", color=col1, elinewidth=0.7)
    ax.scatter(xs1, ys1, size, marker='*', label="Random Vaccination",
               color=col2)
    ax.errorbar(xs1, ys1, yerr=yse1, fmt="|", color=col2, elinewidth=0.7)
    ax.scatter(xs2, ys2, size, marker='*', label="Random High-Deg Vaccination",
               color=col2p)
    ax.errorbar(xs2, ys2, yerr=yse2, fmt="|", color=col2p, elinewidth=0.7)
    ax.scatter(xs3, ys3, size, marker='*', label="Ring Vaccination",
               color=col3)
    ax.errorbar(xs3, ys3, yerr=yse3, fmt="|", color=col3, elinewidth=0.7)
    # ax.scatter(xs4, ys4, size, label="E", color=col3p)
    # ax.errorbar(xs4, ys4, yerr=yse4, fmt="|", color=col3p)
    plt.xticks(locs, xls)
    plt.xlabel("Parameter Setting")

    # plt.text(1, 1, 'All graphs beyond edge limit',
    #          rotation='vertical')

    ax.legend(fontsize=7, frameon=True, loc='bottom middle')

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

    for i in range(len(filenames), end - 1, len(filenames)):
        ax.axvline(x=i + 0.5, ymin=0, ymax=1, linewidth=0.5)

    plt.tight_layout(0.5, 0.25, 0.25)
    fig.savefig('./Output/' + name + '.png')

    f = open('./Output/' + name + '_table' + '.txt', 'w')
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
            f.write(str(mean) + "\t" + str(mean) + '\u00B1' + str(
                diff) + '\t' + str(std) + '\t' + str(m) + "\t")
        f.write("\n")


# Command line calls
main(int(sys.argv[1]), int(sys.argv[2]))

# Run line:
# Num PSs
# Samples per PS
# python make_Combo.py 29 30
