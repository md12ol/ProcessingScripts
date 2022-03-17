import matplotlib.pyplot as plt
import numpy as np

"""
This script gathers data and creates the dist matrix (CIBCB 2020)
"""


def loadData(fname):
    with open(fname) as f:
        lines = f.readlines()
        data = []
        for line in lines:
            line = line.split(',')
            data.append([float(x) for x in line])
            pass
        pass
    return data  # 2d array of matrix from file fname


def main():
    inp_file = "./Input/Distance.dat"
    data = loadData(inp_file)

    rest = []
    for p in range(1, 10):
        for e in range(1, 9):
            rest.append("P" + str(p) + "E" + str(e))
            pass
        pass

    sir_lbls = []
    siir_lbls = []
    for p in range(1,19):
        sir_lbls.append("Prof" + str(p))
        sir_lbls.append("")
        siir_lbls.append("Prof" + str(p))
        siir_lbls.append("")
        pass

    sir_data = [[0.0 for x in range(72)]for y in range(72)]
    for x in range(72):
        for y in range(72):
            sir_data[x][y] = data[x][y]

    bet_data = [[0.0 for x in range(72)]for y in range(72)]
    bet_ymod = -72
    for x in range(72):
        for y in range(72, 144):
            bet_data[x][y + bet_ymod] = data[x][y]

    siir_data = [[0.0 for x in range(72)]for y in range(72)]
    bet_ymod = -72
    bet_xmod = -72
    for x in range(72,144):
        for y in range(72,144):
            siir_data[x + bet_xmod][y + bet_ymod] = data[x][y]

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(bet_data)

    # We want to show all ticks...
    ax.set_xticks(np.arange(3.5,72, 4))
    ax.set_yticks(np.arange(3.5,72, 4))
    # ... and label them with the respective list entries
    ax.set_xticklabels(siir_lbls)
    ax.set_yticklabels(sir_lbls)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center", va="top")
    plt.setp(ax.get_yticklabels(), rotation=90, ha="right", va="center")
    # ax.set_ylabel('SIR Model of Infection')
    # ax.set_xlabel('SIR Model of Infection')

    # Loop over data dimensions and create text annotations.
    # for i in range(len(vegetables)):
    #     for j in range(len(farmers)):
    #         text = ax.text(j, i, harvest[i, j],
    #                        ha="center", va="center", color="w")

    ax.set_title("Column Entropy Distance Between Epidemic Models")
    fig.tight_layout()
    plt.show()
    # fig.savefig('./Output/SIIRvSIIRhm.png')


pass

main()
