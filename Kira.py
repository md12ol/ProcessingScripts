import math
import re
import string

import matplotlib.pyplot as pltt
import numpy as np

"""
Processes folders of output in the form "Output - [Profile Number] w [States], [Population Size], [Mutations]" to 
create boxplots, tables, fitness files, and information about the best parameter settings.
"""

inp = "./Input/"
outp = "./Output/"
finame = "best.dat"
samps = 30
lower_better = True
precision = 6
col_width = 4 + precision


def getFits(dir_path: str, ascending: bool):
    data = []
    with open(dir_path + finame) as f:
        lines = f.readlines()
        for line in lines:
            if line.__contains__(str("fitness")):
                data.append(float(re.findall("\d+\.\d+", line)[0]))
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
    out.write(str(diff).ljust(col_width))
    out.write(str(maxima).ljust(col_width))
    return mean, maxima


def toFile(data: [], fname: string, exp: int):
    out = open(outp + fname + str(exp) + ".dat", "w")
    for d in data:
        out.write(str(d) + "\n")
        pass
    out.close()
    pass


def main():
    # Name of the folder where experiment data is
    folder_name = "Output - Exp 1"

    data = getFits(inp + folder_name + '/', lower_better)

    pltt.rc('xtick', labelsize=6)
    pltt.rc('ytick', labelsize=6)

    fig = pltt.figure()
    fig.set_dpi(500)
    fig.set_figheight(3)

    plt = fig.add_subplot(111)

    plt.boxplot(data)

    fig.suptitle("Boxplot", fontsize=12)
    plt.set_xlabel("Experiment", fontsize=10)
    plt.set_ylabel("Fitness", fontsize=10)
    fig.tight_layout()
    fig.savefig(outp + "boxplot.png")
    print("DONE")
    pass


main()
