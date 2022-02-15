from operator import itemgetter

import matplotlib.pyplot as plt

inp = "./Input/"
outp = "./Output/"
finame = "best.lint"
samps = 30
lower_better = False
precision = 6
col_width = 6 + precision
verts = 256


# Priority
# Edit paper (EA, bitsprayer)
# Networks?

def get_prof(line):
    pts = line.split(":")
    pts_1 = pts[0].split("[")
    start = int(pts_1[1][0:2])
    end = int(pts_1[1][3:5])
    line = pts[1][1:]
    line = line.rstrip("\n")
    n = 0
    prof = []
    # chars = list(line)
    words = [str(line[i:i + 3]) for i in range(0, len(line), 3)]
    for word in words:
        # word = line[n:n+3]
        if word != "   ":
            prof.append(int(word))
        # n+= 3
        pass
    if prof[-1] != 0:
        prof.append(0)
        pass
    return [start, end, prof]


def get_data(dir_path: str):
    fits = []
    var_profs = []
    profiles = []
    edges = []
    with open(dir_path + finame) as f:
        lines = f.readlines()
        next_graph = False
        for line in lines:
            if line.__contains__(str("-fitness")):
                d = line.split(" ")
                fits.append(float(d[0]))
                pass
            elif line.__contains__(str("V")):
                var_profs.append(get_prof(line))
                pass
            elif line.__contains__(str("Graph")):
                profiles.append(var_profs)
                var_profs = []
                next_graph = True
                pass
            elif next_graph:
                next_graph = False
                edges.append(int(line.rstrip("\n").split(" ")[-1]))
                pass
            pass
        pass
    data = [[i, fits[i], profiles[i], edges[i]] for i in range(samps)]
    data.sort(key=itemgetter(0))  # Ascending
    if not lower_better:
        data.reverse()
        pass
    return data


def main():
    print("START")
    folders = []
    mode = ["EL", "ES"]
    probs = ["0.0025", "0.0050", "0.0075", "0.0100"]
    edits = ["04 to 12", "12 to 20", "20 to 28"]
    folds = []
    x_lbl = []

    for mi, m in enumerate(mode):
        m_root = inp + "Output - " + m + " "
        folds.append(m_root + "Base/")
        x_ls = ["Baseline"]
        for pi, p in enumerate(probs):
            p_root = m_root + p + "P and "
            xl = str(float(p) * 100) + "%, "
            for ei, e in enumerate(edits):
                folds.append(p_root + e + "E/")
                x_ls.append(xl + e + "E")
                pass
            pass
        x_lbl.append(x_ls)
        folders.append(folds)
        folds = []
        pass

    mode = ["EL24", "EL16"]
    ext_lbl = ["24B", "16B"]
    probs = ["0.0100"]
    folds = [inp + "Output - EL Base/", inp + "Output - EL 0.0100P and 04 to 12E/",
             inp + "Output - EL 0.0100P and 12 to 20E/", inp + "Output - EL 0.0100P and 20 to 28E/"]
    x_ls = ["Baseline", "32B, 1.0%, 04 to 12E", "32B, 1.0%, 12 to 20E", "32B, 1.0%, 20 to 28E"]
    for mi, m in enumerate(mode):
        m_root = inp + "Output - " + m + " "
        xl_root = ext_lbl[mi] + ", "
        for pi, p in enumerate(probs):
            p_root = m_root + p + "P and "
            xl = xl_root + str(float(p) * 100) + "%, "
            for ei, e in enumerate(edits):
                folds.append(p_root + e + "E/")
                x_ls.append(xl + e + "E")
                pass
            pass
        pass
    x_lbl.append(x_ls)
    folders.append(folds)

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
    extra_len = []
    extra_edges = []
    vars_len = []
    vars_spd = []

    # all_data[func][fold][0-29][0] = run num
    # all_data[func][fold][0-29][1] = run's fit
    # all_data[func][fold][0-29][2] = [run's profiles]
    # all_data[func][fold][0-29][3] = run's edges
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
            net_edgs.append(run[3])
            pass
        avg_len.append(mean_len)
        best_len.append(epi_lens)
        num_edges_len.append(net_edgs)
        vars_len.append(exp_vars)
        pass

    for fold in all_data[1]:
        mean_spread = []
        f_best_spread = []
        net_edges = []
        exp_vars = []
        for run in fold:
            mean_spread.append(run[1])
            run_epi_spread = []
            for prf in run[2]:
                run_epi_spread.append(sum(prf[2]))
                pass
            exp_vars.append(len(run[2]))
            f_best_spread.append(sum(run_epi_spread))
            net_edges.append(run[3])
            pass
        avg_spread.append(mean_spread)
        best_spread.append(f_best_spread)
        num_edges_spread.append(net_edges)
        vars_spd.append(exp_vars)
        pass

    for fold in all_data[2]:
        mean_len = []
        net_edges = []
        for run in fold:
            mean_len.append(run[1])
            net_edges.append(run[3])
            pass
        extra_len.append(mean_len)
        extra_edges.append(net_edges)
        pass

    titles = ["Epidemic Duration", "Epidemic Spread", "Best Epidemic Duration", "Best Epidemic Spread",
              "Network Edges with Epidemic Duration", "Network Edges with Epidemic Spread",
              "Epidemic Duration with 1.0% Variant Probability", "Network Edges with Epidemic Duration",
              "Number of Variants with Epidemic Duration", "Number of Variants with Epidemic Spread"]
    names = ["EL_boxplot", "ES_boxplot", "BestEL_boxplot", "BestES_boxplot", "EdgesEL_boxplot", "EdgesES_boxplot",
             "ExtraEL_boxplot", "ExtraEdgesEL_boxplot", "VariantsEL_boxplot", "VariantsES_boxplot"]
    data = [avg_len, avg_spread, best_len, best_spread, num_edges_len, num_edges_spread, extra_len, extra_edges,
            vars_len, vars_spd]
    lbls = [x_lbl[0], x_lbl[1], x_lbl[0], x_lbl[1], x_lbl[0], x_lbl[1], x_lbl[2], x_lbl[2], x_lbl[0], x_lbl[1]]
    xsp = [[i for i in range(len(all_data[0]))], [i for i in range(len(all_data[1]))],
           [i for i in range(len(all_data[2]))]]
    xpos = [xsp[0], xsp[1], xsp[0], xsp[1], xsp[0], xsp[1], xsp[2], xsp[2], xsp[0], xsp[1]]
    ylb = ["Fitness", "Fitness", "Best Epidemic Duration", "Best Epidemic Spread", "Number of Edges",
           "Number of Edges", "Fitness", "Number of Edges", "Number of Variants", "Number of Variants"]
    xlb = ["Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Initial Variant Bits, Variant Probability, Variant Edits)",
           "Parameter Setting (Initial Variant Bits, Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)",
           "Parameter Setting (Variant Probability, Variant Edits)"]

    print("TEST")

    for idx in range(len(titles)):
        plt.rc('xtick', labelsize=6)
        plt.rc('ytick', labelsize=6)

        f = plt.figure()
        f.set_dpi(500)
        f.set_figheight(5)

        plot = f.add_subplot(111)

        plot.boxplot(data[idx], positions=xpos[idx])
        plot.set_xticks(xpos[idx])
        plot.set_xticklabels(lbls[idx], rotation=90)

        f.suptitle(titles[idx], fontsize=12)
        plot.set_xlabel(xlb[idx], fontsize=10)
        plot.set_ylabel(ylb[idx], fontsize=10)
        f.tight_layout()
        f.savefig(outp + names[idx] + ".png")
    print("DONE")

    profs_EL = all_data[0][-1][0][2]
    profs_ES = all_data[1][-1][0][2]
    f = plt.figure()
    f.set_dpi(500)
    f.set_figheight(5)

    plot = f.add_subplot(111)

    xs = []
    ys = []
    for prof in profs_EL:
        xs.append(prof[2])
        ys.append([i for i in range(prof[0], prof[1] + 1)])
        pass

    for idx in range(len(profs_EL)):
        plot.plot(ys[idx], xs[idx], label="V" + str(idx))
        pass

    f.savefig(outp + "EL_profile.png")
    pass


main()
