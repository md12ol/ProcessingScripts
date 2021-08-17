from graphviz import Graph

"""
Takes in files representing the adjacency lists of networks and creates visualizations of the networks.
"""

out_root = "./Output/"
inp_root = "./Input/"
verts = 512


def loadData(fName):
    data = []
    with open(fName) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(" ")
            for to_node in line:
                data.append([from_node, int(to_node)])
                pass
            pass
        pass
    return data


def makeGraph():
    inp_file = "Output/EXP1_graph.dat"
    out_file = "outGraph0"
    data = loadData(inp_file)

    g = Graph(engine='sfdp')
    g.attr(size="8,8")
    g.graph_attr.update(dpi='600')
    g.node_attr.update(shape='point', width='0.01', height='0.01')
    g.edge_attr.update(color='black', penwidth='0.2')
    for n in range(verts):
        if n == 0:
            g.node(str(n), label=str(n), color='red')
        else:
            g.node(str(n), label=str(n))
        pass

    for d in data:
        if int(d[0]) >= int(d[1]):
            g.edge(str(d[0]), str(d[1]))
            pass
        pass

    g.render(filename=out_file, directory='Output/', cleanup=False, format='png')
    pass


def main():
    makeGraph()
    pass


main()
