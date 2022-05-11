import math
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np

inp = "./Input/"
outp = "./Output/"
finame = "best.lint"
samps = 30
lower_better = False
precision = 6
col_width = 6 + precision
verts = 256


def get_prof(line):
    pts = line.split(":")
    pts_1 = pts[0].split("[")
    info = pts_1[0][0:7]
    start = int(pts_1[1][0:2])
    pts_1 = pts_1[1].split("-")
    end = int(pts_1[1][0:2])
    line = pts[1][1:]
    line = line.rstrip("\n")
    n = 0
    prof = []
    # chars = list(line)
    words = line.split("\t")
    for word in words:
        if word != '':
            prof.append(int(word))
            pass
    return [start, end, prof, info]


def get_dna(line):
    line = line.rstrip("\n").split("\t")[1]
    return line


def get_data(dir_path: str):
    fits = []
    var_profs = []
    var_dnas = []
    profiles = []
    dnas = []
    edges = []
    with open(dir_path + finame) as f:
        lines = f.readlines()
        next_graph = False
        for line in lines:
            if line.__contains__(str("-fitness")):
                d = line.split(" ")
                fits.append(float(d[0]))
                pass
            elif line.__contains__(str("[")):
                var_profs.append(get_prof(line))
                pass
            elif line.__contains__(str("V")):
                var_dnas.append(get_dna(line))
                pass
            elif line.__contains__(str("Graph")):
                profiles.append(var_profs)
                var_profs = []
                dnas.append(var_dnas)
                var_dnas = []
                next_graph = True
                pass
            elif next_graph:
                next_graph = False
                edges.append(int(line.rstrip("\n").split("\t")[-1]))
                pass
            pass
        pass
    # run number, fitness, profileS, dnaS, edge count
    data = [[i, fits[i], profiles[i], dnas[i], edges[i]] for i in range(samps)]
    data.sort(key=itemgetter(1))  # Ascending
    if not lower_better:
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


def make_table(many_data: [], exp_info: [], fname: str):
    with open(fname, "w") as f:
        f.write("EXP".ljust(col_width))
        f.write("Parameters".ljust(2 * col_width))
        f.write("Best Run".ljust(col_width))
        f.write("Mean".ljust(col_width))
        f.write("SD".ljust(col_width))
        f.write("95% CI".ljust(col_width))
        f.write("Best".ljust(col_width))
        f.write("\n")
        for di, data in enumerate(many_data):
            f.write(str("EXP" + str(di + 1)).ljust(col_width))
            f.write(exp_info[di].ljust(2 * col_width))
            f.write(str("Run " + str(data[0][0])).ljust(col_width))
            d = [data[i][1] for i in range(samps)]
            writeStat(d, f)
            f.write("\n")
            pass
        pass
    pass


def write_best(data: [], info: str, seed: str):
    with open(seed, "w") as f:
        f.write("Run " + str(data[0][0]) + "\n")
        f.write(str(data[0][1]) + "\n")
        f.write(info + "\n")
        profs = data[0][2]
        for prof in profs:
            pstr = ""
            idx = 0
            while idx < prof[0]:
                pstr += "\t"
                idx += 1
                continue
            for p in prof[2]:
                pstr += str(p) + "\t"
                pass
            f.write(pstr)
            f.write("\n")
            pass
        dnas = data[0][3]
        for dna in dnas:
            f.write(dna)
            f.write("\n")
            pass
        pass
    pass


def main():
    print("START")
    folders = []
    # mode = ["EL", "ES"]
    # inits = ["08", "16", "24", "32"]
    # probs = ["0.0025", "0.0050", "0.0075", "0.0100"]
    mode = ["EL"]
    inits = ["08", "16", "24", "32"]
    probs = ["0.0025", "0.0050", "0.0075", "0.0100"]
    edits = ["04-12", "12-20", "20-28", "28-36"]
    folds = []
    x_lbl = []
    plt.style.use("seaborn-dark")

    for mi, m in enumerate(mode):
        m_root = inp + "Output - " + m
        # folds.append(m_root + " Base/")
        m_root = m_root + " 050P, "
        # x_ls = ["Baseline"]
        x_ls = []
        for ii, i in enumerate(inits):
            i_root = m_root + i + "I, "
            xli_root = str(int(i)) + "I, "
            for pi, p in enumerate(probs):
                p_root = i_root + p + "%, "
                xl = xli_root + str(float(p) * 100) + "%, "
                for ei, e in enumerate(edits):
                    folds.append(p_root + e + "E/")
                    x_ls.append(xl + e + "E")
                    pass
                pass
            pass
        x_lbl.append(x_ls)
        folders.append(folds)
        folds = []
        pass

    all_data = []
    for flds in folders:
        data = []
        for f in flds:
            data.append(get_data(f))
            pass
        all_data.append(data)
        pass

    avg_len = []
    avg_spread = []
    best_len = []
    best_spread = []
    num_edges_len = []
    num_edges_spread = []
    vars_len = []
    vars_spd = []

    # all_data[func][fold][0-29][0] = run num
    # all_data[func][fold][0-29][1] = run's fit
    # all_data[func][fold][0-29][2] = [run's profiles][#] = {start, end, [profile]}
    # all_data[func][fold][0-29][3] = [run's dnas][#] = [dna]
    # all_data[func][fold][0-29][4] = run's edges
    for fold in all_data[0]:
        mean_len = []
        epi_lens = []
        net_edgs = []
        exp_vars = []
        for run in fold:
            mean_len.append(run[1])
            run_epi_lens = []
            for prf in run[2]:
                run_epi_lens.append(prf[1])
                pass
            exp_vars.append(len(run[2]))
            epi_lens.append(max(run_epi_lens))
            net_edgs.append(run[4])
            pass
        avg_len.append(mean_len)
        best_len.append(epi_lens)
        num_edges_len.append(net_edgs)
        vars_len.append(exp_vars)
        pass

    # for fold in all_data[1]:
    #     mean_spread = []
    #     f_best_spread = []
    #     net_edges = []
    #     exp_vars = []
    #     for run in fold:
    #         mean_spread.append(run[1])
    #         run_epi_spread = []
    #         for prf in run[2]:
    #             run_epi_spread.append(sum(prf[2]))
    #             pass
    #         exp_vars.append(len(run[2]))
    #         f_best_spread.append(sum(run_epi_spread))
    #         net_edges.append(run[4])
    #         pass
    #     avg_spread.append(mean_spread)
    #     best_spread.append(f_best_spread)
    #     num_edges_spread.append(net_edges)
    #     vars_spd.append(exp_vars)
    #     pass

    # titles = ["Epidemic Duration", "Epidemic Spread"]
    # names = ["EL_boxplot", "ES_boxplot"]
    # data = [avg_len, avg_spread]
    # lbls = [x_lbl[0], x_lbl[1]]
    # xsp = [[i for i in range(len(all_data[0]))], [i for i in range(len(all_data[1]))]]
    # xpos = [xsp[0], xsp[1]]
    # ylb = ["Fitness", "Fitness"]
    # xlb = ["Experiment (Initial Variant Bits, New Variant Probability", "Variant Edits"]

    titles = ["Epidemic Duration"]
    names = ["EL_boxplot"]
    data = [avg_len]
    lbls = [x_lbl[0]]
    xsp = [[i for i in range(len(all_data[0]))]]
    xpos = [xsp[0]]
    ylb = ["Fitness"]
    xlb = ["Experiment (Initial Variant Bits, New Variant Probability", "Variant Edits)"]

    for idx in range(len(titles)):
        plt.rc('xtick', labelsize=6)
        plt.rc('ytick', labelsize=6)

        f = plt.figure()
        f.set_dpi(450)
        f.set_figheight(5)
        f.set_figwidth(8)

        plot = f.add_subplot(111)

        plot.boxplot(data[idx], positions=xpos[idx])
        plot.set_xticks(xpos[idx])
        plot.set_xticklabels(lbls[idx], rotation=90)

        f.suptitle(titles[idx], fontsize=12)
        plot.set_xlabel(xlb[idx], fontsize=10)
        plot.set_ylabel(ylb[idx], fontsize=10)
        f.tight_layout()
        f.savefig(outp + names[idx] + ".png", dpi=450)
        plt.close()
        pass

    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)
    for fidx, many_data in enumerate(all_data):
        make_table(many_data, x_lbl[fidx], outp + mode[fidx] + "_table.dat")
        for didx, data in enumerate(many_data):
            profs = data[0][2]
            f = plt.figure()
            f.set_figheight(5)
            f.set_figwidth(8)

            plot = f.add_subplot(111)

            xs = []
            ys = []

            for prof in profs:
                xs.append(prof[2])
                ys.append([i for i in range(prof[0], prof[1] + 1)])
                pass

            for idx in range(len(profs)):
                if idx == 0:
                    # lbl = "Initial Variant"
                    lbl = profs[idx][3]
                else:
                    # lbl = "Variant " + str(idx)
                    lbl = profs[idx][3]
                plot.plot(ys[idx], xs[idx], label=lbl)
                pass

            f.suptitle(mode[fidx] + " Experiment " + str(didx + 1) + " Epidemic Curve")
            plot.set_xlabel("Day", fontsize=12)
            plot.set_ylabel("New Infections", fontsize=12)
            plot.minorticks_on()
            plot.grid(visible="True", axis="x", which='minor', color="darkgray", linewidth=0.5)
            plot.grid(visible="True", axis="x", which='major', color="black", linewidth=0.75)
            plot.grid(visible="True", axis="y", which='major', color="black", linewidth=0.75)
            plt.legend(bbox_to_anchor=(0.5, 1), loc="lower center", ncol=6, borderaxespad=0)
            f.tight_layout()
            f.savefig(outp + mode[fidx] + "_EXP" + str(didx + 1) + "_profile.png", dpi=450)
            plt.close()
            write_best(data, x_lbl[fidx][didx], outp + mode[fidx] + "_EXP" + str(didx + 1) + "_best.dat")
            pass
        pass

    # profs_EL = all_data[0][-1]

    print("END")
    pass


main()
