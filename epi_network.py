import os
import re

from graphviz import Graph

"""
Takes in files representing the adjacency lists of networks and creates visualizations of the networks.
"""

out_root = "./Output/"
inp_root = "./Input/"
file_root = "/outGraph"
files_per_folder = 30
folder_root = "profile"
profiles = 9
verts = 128
ignore_lines = 1


def loadData(fName: str):
    data = []
    with open(fName) as f:
        lines = f.readlines()
        for _ in range(ignore_lines):
            lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split("\t")
            for to_node in line:
                data.append([from_node, int(to_node)])
                pass
            pass
        pass
    return data


def makeGraph(file_in: str, dir: str, fnum: int):
    out_file = "outGraph" + str(fnum)
    data = loadData(file_in)

    g = Graph(engine='sfdp')
    g.attr(size="6,6")
    g.graph_attr.update(dpi='600', overlap='false', splines='true')
    g.node_attr.update(shape='circle', style='filled', fontsize='12', fixedsize='true')
    g.edge_attr.update()
    for n in range(verts):
        if n == 0:
            g.node(str(n), label=str(n), fillcolor='red')
        elif n < verts / 4:
            g.node(str(n), label=str(n), fillcolor='cyan')
        elif n < verts / 2:
            g.node(str(n), label=str(n), fillcolor='orange')
        elif n < 3 * verts / 4:
            g.node(str(n), label=str(n), fillcolor='yellow')
        else:
            g.node(str(n), label=str(n), fillcolor='green')

    for d in data:
        if int(d[0]) >= int(d[1]):
            g.edge(str(d[0]), str(d[1]))
            pass
        pass

    g.render(filename=out_file, directory=dir, cleanup=True, format='png')
    pass


def main():
    for didx, dire in enumerate(os.listdir(inp_root)):
        with open(inp_root + dire + "/" + "best.lint") as o:
            lines = o.readlines()
            lline = lines[-1]
            words = lline.split(" ")
            val = re.search("run\\d+\\.dat", words[1]).group(0)
            val = re.search("\\d+", val).group(0)
            makeGraph(inp_root + dire + "/" + "Graph" + str(val) + ".dat", out_root, didx)
            pass
        print(str(didx) + "DONE")
    # inp_file = inp_root + "exp3/Graph0.dat"
    # out_folder = out_root
    # makeGraph(inp_file, out_folder, 3)


# for pnum in range(1, profiles + 1):
#     for fnum in range(files_per_folder):
#         inp_file = inp_root + folder_root + str(pnum) + file_root + str(file_root) + ".dat"
#         out_folder = out_root + folder_root + str(pnum) + "/"
#         makeGraph(inp_file, out_folder, fnum)
#         pass
#     pass
# pass


main()
