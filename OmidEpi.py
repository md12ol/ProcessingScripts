import math
import re
import string
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np

inp = "./Input/"
outp = "./Output/"
finame = "best.lint"
samps = 30
lower_better = False
precision = 6
col_width = 7 + precision
num_exps = 8
exp_root = "exp"


def getFits(dir_path: str, ascending: bool):
    data = []
    with open(dir_path + finame) as f:
        lines = f.readlines()
        for line in lines:
            if line.__contains__(str("fitness")):
                li = re.findall("\d+\.?\d+", line)
                data.append(float(li[-1]))
                pass
            pass
        pass
    data.sort()  # Ascending
    if not ascending:
        data.reverse()
        pass
    return data


def writeStat(data: [], out):
    mean = float(np.mean(data))
    mean = round(mean, precision)
    std = float(np.std(data, ddof=0))
    std = round(std, precision)  # Population standard deviation
    diff = 1.96 * std / math.sqrt(30)  # 95% CI
    diff = round(diff, precision)
    if lower_better:
        maxima = float(min(data))
        pass
    else:
        maxima = float(max(data))
        pass
    maxima = round(maxima, precision)
    out.write(str(mean).ljust(col_width))
    out.write(str(std).ljust(col_width))
    out.write(str(u'\u00B1' + str(diff)).ljust(col_width))
    out.write(str(maxima).ljust(col_width))
    return mean, maxima


def toFile(data: [], fname: string, exp: int, stats: [], inf: str):
    out = open(outp + fname + str(exp) + ".dat", "w")
    out.write(inf + '\n')
    out.write("Mean: " + str(stats[0]) + '\n')
    out.write("Best: " + str(stats[1]) + '\n')
    for d in data:
        out.write(str(d) + "\n")
        pass
    out.close()
    pass


def main():
    exps = [i for i in range(8)]

    # Collect the data
    f_root = inp + exp_root

    # Create data[profile][states][popsize][mutations] = 30 fitness vals
    # tables = []
    # tab_root = outp + "table_"
    data = [[] for _ in range(num_exps + 1)]
    folder = inp + "SIRBest/"
    data[0] = getFits(folder, lower_better)
    for exp in exps:
        folder = f_root + str(exp) + "/"
        data[exp + 1] = getFits(folder, lower_better)
    pass

    # Process the data and make table
    col_ws = [6]
    means = []
    bests = []
    data_1d = []
    out = open(outp + "EXP Summary.dat", "w", encoding='utf-16')
    out.write("EXP".ljust(col_ws[0]))
    out.write("Mean".ljust(col_width))
    out.write("SD".ljust(col_width))
    out.write("95%CI".ljust(col_width))
    out.write("Best".ljust(col_width))
    out.write('\n')
    for exp, dat in enumerate(data):
        assert len(dat) == samps
        data_1d.append(dat)
        out.write(str("EXP" + str(exp - 1)).ljust(col_ws[0]))
        vals = writeStat(dat, out)
        out.write('\n')
        toFile(dat, "EXP", exp - 1, vals, "EXP" + str(exp - 1))
        if exp - 1 >= 0:
            means.append([vals[0], exp - 1])
            bests.append([vals[1], exp - 1])
            pass
        pass
    out.close()

    means.sort(key=itemgetter(0))
    bests.sort(key=itemgetter(0))

    if not lower_better:
        means.reverse()
        bests.reverse()

    out = open(outp + "best.dat", "w")
    # for idx in range(len(profs)):
    # out.write("Profile " + str(profs[idx]) + "\n")
    out.write("Best Mean: ")
    out.write(str(means[0][0]) + "\n")
    out.write("EXP: " + str(means[0][1]) + "\n")
    out.write("Best Fitness: ")
    out.write(str(bests[0][0]) + "\n")
    out.write("EXP: " + str(bests[0][1]) + "\n")
    out.write("\n")
    out.close()

    x_labels = ["SIR PS1"]
    for exp in range(num_exps):
        x_labels.append("SIVR PS" + str(exp + 1))
        pass

    fig_root = outp + "boxplot"
    plt.rc('xtick', labelsize=6)
    plt.rc('ytick', labelsize=6)

    f = plt.figure()
    f.set_dpi(500)
    f.set_figheight(4)

    plot = f.add_subplot(111)
    plot.boxplot(data_1d)
    plot.set_xticklabels(x_labels, fontsize=10, rotation=90)

    f.suptitle("SIR v. SIVR", fontsize=15)
    plot.set_xlabel("Experiment", fontsize=12)
    plot.set_ylabel("Distribution of Fitness", fontsize=12)
    f.tight_layout()
    # f.subplots_adjust(left=.08, bottom=.1, right=.98, top=.91, wspace=0, hspace=0)
    f.savefig(fig_root + ".png")
    return 0


main()
