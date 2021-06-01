import math

from graphviz import Graph

"""
Takes in files representing the adjacency lists of networks and creates visualizations of the networks.
"""

out_root = "./Output/"
inp_root = "./Input/"
verts = 160
edge_w = "1"


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
    graph_root = "initGraph_"
    exp_strs = ["Ring", "PLC"]
    theta_diff = 2 * math.pi / (verts / 2)
    inside_offset = theta_diff / 2
    radius = [3, 2.5]

    for sidx, estr in enumerate(exp_strs):
        inp_file = inp_root + graph_root + estr + ".dat"
        out_file = graph_root + estr
        data = loadData(inp_file)

        if sidx == 0:
            g = Graph(engine='neato')
            g.attr(size="5,5")
            g.graph_attr.update(dpi='600')
            g.node_attr.update(fixedsize='true', width='0.1', shape='point', fillcolor='white', pin='true')
            g.edge_attr.update(weight=edge_w)
            outer = 0
            theta = 0
            for n in range(verts):
                x_val = radius[outer] * math.cos(theta)
                y_val = radius[outer] * math.sin(theta)
                pos = str(x_val) + "," + str(y_val) + "!"
                g.node(str(n), pos=pos)
                outer = (outer + 1) % 2
                theta += inside_offset
                pass
            pass
        else:
            g = Graph(engine='sfdp')
            g.attr(size="7,7")
            g.graph_attr.update(dpi='600', K='0.55', ratio='1', splines='true', overlap='false')
            g.node_attr.update(fixedsize='true', shape='point', fillcolor='white', width='0.075')
            g.edge_attr.update(weight=edge_w)
            for n in range(verts):
                g.node(str(n))
                pass
            pass

        # for n in range(32, 64):
        #     g.node(str(n), fillcolor='orange')
        #     pass
        #
        # for n in range(64, 96):
        #     g.node(str(n), fillcolor='yellow')
        #     pass
        #
        # for n in range(96, 128):
        #     g.node(str(n), fillcolor='green')
        #     pass

        for d in data:
            if d[0] >= d[1]:
                g.edge(str(d[0]), str(d[1]), penwidth=str(edge_w))
                pass
            pass

        g.render(filename=out_file, directory='Output/', cleanup=True, format='png')
        pass
    pass


def main():
    makeGraph()
    pass


main()
