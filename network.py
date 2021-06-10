import math

from graphviz import Graph

"""
Takes in files representing the adjacency lists of networks and creates visualizations of the networks.
"""

out_root = "./Output/"
inp_root = "./Input/"
verts = 128


def loadData(fName):
    data = []
    with open(fName) as f:
        lines = f.readlines()
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


def makeGraph():
    inp_file = inp_root + "outGraph0.dat"
    out_file = "outGraph0"
    data = loadData(inp_file)

    g = Graph(engine='sfdp')
    # g.attr(size="5,5")
    g.graph_attr.update(dpi='600', overlap='false')
    g.node_attr.update()
    g.edge_attr.update()
    for n in range(verts):
        g.node(str(n), label=str(n))
        pass

    for d in data:
        if int(d[0]) >= int(d[1]):
            g.edge(str(d[0]), str(d[1]))
            pass
        pass

    g.render(filename=out_file, directory='Output/', cleanup=True, format='png')
    pass


def main():
    makeGraph()
    pass


main()
