"""
Process folders of output in the form "G[Graph Number] Output - [States]S, [Popsize]P, [Mutations]M"
to create boxplots, tables, ...
"""
import math
import re
import shutil
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
from graphviz import Graph

inp = "./Input/"
outp = "./Output/"
finame = "best.sda"
samps = 30
lower_better = True
precision = 6
col_width = 6 + precision
verts = 512


def get_data(dir_path: str):
    data = []
    with open(dir_path + finame) as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            if line.__contains__(str("Actual Fitness:")):
                d = re.findall("\\[(.*?)]", line)
                d = d[0].split(", ")
                d = list(map(int, d))
                data.append([d, count])
                count += 1
                pass
            pass
        pass
    data.sort(key=itemgetter(0))  # Ascending
    if not lower_better:
        data.reverse()
        pass
    return data


def to_file(data: [], filename: str, exp: int, stats: [], inf: str):
    out = open(outp + filename + str(exp) + ".dat", "w")
    out.write(inf + '\n')
    out.write("Diameter Mean: " + str(stats[0]) + '\n')
    out.write("Edge Mean: " + str(stats[1]) + '\n')
    out.write("Best: " + str(stats[2]) + '\n')
    out.write("Best Run: " + str(stats[3]) + '\n')
    for d in data:
        out.write(str(d) + "\n")
        pass
    out.close()
    pass


def write_stat(data: [], out1, out2):
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
    out1.write(str(mean).ljust(col_width))
    out1.write(str(std).ljust(col_width))
    out1.write(str(diff).ljust(col_width))
    out2.write(str(mean).ljust(col_width))
    out2.write(str(std).ljust(col_width))
    out2.write(str(diff).ljust(col_width))
    return mean, maxima


def box_plot(data, locs, edge_color, fill_color):
    bp = plt.boxplot(data, positions=locs, patch_artist=True)

    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)

    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)

    return bp


def edge_list(filename):
    el = []
    with open(filename) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(" ")
            for to_node in line:
                el.append([from_node, int(to_node)])
                pass
            pass
        pass
    return el


def make_graph(el: [], out_file: str):
    g = Graph(engine='sfdp')

    g.graph_attr.update(dpi='1000', size="8,8")
    g.node_attr.update(shape='point', width='0.01', height='0.01')
    g.edge_attr.update(color='black', penwidth='0.2')
    for n in range(verts):
        if n == 0:
            g.node(str(n), label=str(n), color='red')
        else:
            g.node(str(n), label=str(n))
        pass

    for d in el:
        if int(d[0]) >= int(d[1]):
            g.edge(str(d[0]), str(d[1]))
            pass
        pass

    g.render(filename=out_file, directory=outp, cleanup=True, format='png')
    pass


def main():
    graphs = [1, 2, 3]
    states = [8, 12, 16]
    pops = [36, 72]
    muts = [2, 3, 4]

    # Create data[Graph][States][Pops][Muts] = 30 sorted with [0 = diam, 1 = edges]
    data = [[[[[] for _ in muts] for _ in pops] for _ in states] for _ in graphs]
    tables = []
    t_root = outp + "table_G"
    for gi, g in enumerate(graphs):
        g_root = inp + "G" + str(g) + " Output - "
        out_file = t_root + str(g) + ".dat"
        tables.append(open(out_file, "w"))
        for si, s in enumerate(states):
            s_root = g_root + str(s).zfill(2) + "S, "
            for pi, p in enumerate(pops):
                p_root = s_root + str(p) + "P, "
                for mi, m in enumerate(muts):
                    fold = p_root + str(m) + "M/"
                    data[gi][si][pi][mi] = get_data(fold)
                    pass
                pass
            pass
        pass

    # Process data and make tables
    cw = [6, 4, 5, 5, 4]
    files = ["Dungeon", "graph"]
    file_ends = [".eps", ".dat"]
    # means[Graph][Exp][0 = diam, 1 = edges]
    means = [[[] for _ in range(2)] for _ in graphs]
    bests = [[] for _ in graphs]
    gs = [[] for _ in graphs]
    exp = 1
    data_1d = [[[] for _ in range(2)] for _ in graphs]
    out = open(outp + "EXP Summary.dat", "w")
    out.write("EXP".ljust(cw[0]))
    out.write("G".ljust(cw[1]))
    out.write("S".ljust(cw[2]))
    out.write("P".ljust(cw[3]))
    out.write("M".ljust(cw[4]))
    out.write("DMean".ljust(col_width))
    out.write("DSD".ljust(col_width))
    out.write("D95%CI".ljust(col_width))
    out.write("EMean".ljust(col_width))
    out.write("ESD".ljust(col_width))
    out.write("E95%CI".ljust(col_width))
    out.write("Best".ljust(col_width))
    out.write('\n')
    for gi, g in enumerate(graphs):
        column = 1
        line_g = str("G" + str(g)).ljust(cw[column])
        for si, s in enumerate(states):
            column = 2
            line_s = line_g + str(str(s) + "S").ljust(cw[column])
            for pi, p in enumerate(pops):
                column = 3
                line_p = line_s + str(str(p) + "P").ljust(cw[column])
                for mi, m in enumerate(muts):
                    column = 4
                    exp_info = str("EXP" + str(exp)).ljust(cw[0])
                    exp_info += line_p + str(str(m) + "M").ljust(cw[column])
                    out.write(exp_info)
                    tables[gi].write(exp_info)  # add exp data
                    raw_dat = data[gi][si][pi][mi]
                    dat = []
                    best_run = raw_dat[0][1]
                    for d in raw_dat:
                        dat.append(d[0])
                    assert len(dat) == samps
                    d_dat, e_dat = [], []
                    for vs in dat:
                        d_dat.append(vs[0])
                        e_dat.append(vs[1])
                    data_1d[gi][0].append(d_dat)
                    data_1d[gi][1].append(e_dat)
                    d_vals = write_stat(d_dat, tables[gi], out)
                    e_vals = write_stat(e_dat, tables[gi], out)
                    out.write(str(dat[0]) + '\n')
                    tables[gi].write(str(dat[0]) + '\n')
                    stats = [d_vals[0], e_vals[0], dat[0], best_run]
                    to_file(dat, "EXP", exp, stats, exp_info)
                    means[gi][0].append([d_vals[0], [si, pi, mi, best_run]])
                    means[gi][1].append([e_vals[0], [si, pi, mi, best_run]])
                    bests[gi].append([[dat[0], e_vals[0]], [si, pi, mi, best_run]])
                    folder = inp + "G" + str(g) + " Output - " + str(s).zfill(2) + "S, " \
                             + str(p) + "P, " + str(m) + "M/"
                    for fi, f in enumerate(files):
                        src = folder + f + str(best_run).zfill(2) + file_ends[fi]
                        dst = outp + "EXP" + str(exp) + "_" + f + file_ends[fi]
                        if f == "graph":
                            gs[gi].append(dst)
                            pass
                        shutil.copyfile(src, dst)
                    exp += 1
                    pass
                pass
            pass
        pass

    out.close()
    for t in tables:
        t.close()
        pass

    for gi in range(len(graphs)):
        means[gi][0].sort(key=itemgetter(0))
        means[gi][1].sort(key=itemgetter(0))
        bests[gi].sort(key=itemgetter(0))
        pass

    for gi, g in enumerate(graphs):
        out = open(outp + "G" + str(g) + "best.dat", "w")
        out.write("Best Diameter Mean: ")
        out.write(str(means[gi][0][0][0]) + "\n")
        out.write("States: " + str(states[int(means[gi][0][0][1][0])]) + "\n")
        out.write("Population: " + str(pops[int(means[gi][0][0][1][1])]) + "\n")
        out.write("Mutations: " + str(muts[int(means[gi][0][0][1][2])]) + "\n")
        out.write("Run: " + str(int(means[gi][0][0][1][3])) + "\n")
        out.write("Best Edge Mean: ")
        out.write(str(means[gi][1][0][0]) + "\n")
        out.write("States: " + str(states[int(means[gi][1][0][1][0])]) + "\n")
        out.write("Population: " + str(pops[int(means[gi][1][0][1][1])]) + "\n")
        out.write("Mutations: " + str(muts[int(means[gi][1][0][1][2])]) + "\n")
        out.write("Run: " + str(int(means[gi][1][0][1][3])) + "\n")
        out.write("Best Fitness (and Lowest Edge Mean): ")
        out.write(str(bests[gi][0][0][0]) + "\n")
        out.write("States: " + str(states[int(bests[0][0][1][0])]) + "\n")
        out.write("Population: " + str(pops[int(bests[0][0][1][1])]) + "\n")
        out.write("Mutations: " + str(muts[int(bests[0][0][1][2])]) + "\n")
        out.write("Run: " + str(int(bests[0][0][1][3])) + "\n")
        out.close()
        pass

    d_locs = []
    e_locs = []
    x_locs = []
    lbls = []
    count = 1
    for si, s in enumerate(states):
        for pi, p in enumerate(pops):
            for mi, m in enumerate(muts):
                lbls.append("S=" + str(s) + " P=" + str(p) + " M=" + str(m))
                d_locs.append(count)
                e_locs.append(count + 1)
                x_locs.append(count + 0.5)
                count += 1
                pass
            pass
        pass

    for gi, g in enumerate(graphs):
        fig_root = outp + "boxplot_G" + str(g)
        plt.rc('xtick', labelsize=6)
        plt.rc('ytick', labelsize=6)

        f = plt.figure()
        f.set_dpi(500)
        f.set_figheight(5)

        plot = f.subplots()
        # bp1 = box_plot(data_1d[gi][0], d_locs, 'red', 'tan')
        # bp2 = box_plot(data_1d[gi][1], d_locs, 'blue', 'cyan')
        # plot.legend([bp1["boxes"][0], bp2["boxes"][0]], ['Diameter', '# Edges'])
        plot.boxplot(data_1d[gi][1])
        plot.set_xticks(d_locs)
        plot.set_xticklabels(lbls, rotation=90)

        f.suptitle("Dungeon with Doors on Dungeon " + str(g), fontsize=12)
        plot.set_xlabel("Parameter Setting (S=states, P=population, M=max. mutations)", fontsize=10)
        plot.set_ylabel("Distribution of Fitness", fontsize=10)
        f.tight_layout()
        # f.subplots_adjust(left=.08, bottom=.1, right=.98, top=.91, wspace=0, hspace=0)
        f.savefig(fig_root + ".png")
        pass

    exp = 1
    for gi, g in enumerate(graphs):
        for g_in in gs[gi]:
            el = edge_list(g_in)
            make_graph(el, "EXP" + str(exp) + "_graph")
            print("Graph (" + str(g) + ", " + str(exp) + ") printed.")
            exp += 1
            pass

    breakpoint = "yes"
    print("Script Complete.")
    return 0


main()
