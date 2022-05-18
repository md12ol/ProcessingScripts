import matplotlib.pyplot as plt

"""
Creates new line graphs for epidemic curves.
"""

inp = "./Profiles/"
outp = "./Output/"
num_profs = 9
tick_size = 14
label_size = 16
title_size = 18


def getData(dir_path: str, pnum: int):
    data = []
    with open(dir_path + "Profile" + str(pnum) + ".dat") as f:
        lines = f.readlines()
        for line in lines:
            data.append(int(line) * 2)
            pass
        pass
    return data


def main():
    prof_nums = [1]
    prof_lbls = ["Epidemic Profile"]
    profs = [[1] for _ in range(len(prof_nums))]
    for idx, p in enumerate(prof_nums):
        profs[idx].extend(getData(inp, p))
        pass

    fig_root = outp
    plt.rc('xtick', labelsize=tick_size)
    plt.rc('ytick', labelsize=tick_size)
    figs = [plt.figure() for _ in range(len(profs))]
    plts = [figs[idx].add_subplot(111) for idx in range(len(profs))]
    x_vals = [x for x in range(len(profs[0]))]

    for idx in range(len(profs)):
        figs[idx].suptitle(prof_lbls[idx], fontsize=title_size)
        plts[idx].plot(x_vals, profs[idx], "o-", linewidth=2)
        plts[idx].set_xlabel("Time Step", fontsize=label_size)
        plts[idx].set_ylabel("New Infections", fontsize=label_size)
        figs[idx].tight_layout()
        figs[idx].savefig(fig_root + prof_lbls[idx] + ".png")
        pass
    pass


main()
