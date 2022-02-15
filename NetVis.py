from graphviz import Graph

outp = "./"
verts = 256
lower_better = True


def high_low_deg(el: []):
    deg = [0 for _ in range(verts)]
    low_deg = []
    high_deg = []
    for ed in el:
        deg[ed[0]] += 1
        deg[ed[1]] += 1
    for idx, deg in enumerate(deg):
        if deg == 1:
            low_deg.append(idx)
            pass
        if deg > 8:
            high_deg.append(idx)
            pass
        pass
    return low_deg, high_deg


def edge_list(filename):
    el = []
    with open(filename) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split(" ")
            for to_node in line:
                if to_node != '':
                    if [from_node, int(to_node)] not in el:
                        if [int(to_node), from_node] not in el:
                            el.append([from_node, int(to_node)])
                            pass
                        pass
                    pass
                pass
            pass
        pass
    return el


def ring_el():
    el = []
    for n in range(verts):
        el.append([n, (n + 1) % verts])
        el.append([n, (n + 2) % verts])
    return el


def make_graph(el: [], low_deg: [], high_deg: [], out_file: str):
    g = Graph(engine='fdp')
    e_cout = 0

    g.graph_attr.update(dpi='1000', size="8,8", outputorder='edgesfirst', overlap='false', splines='true')
    g.node_attr.update(shape='point', width='0.02', height='0.02')
    g.edge_attr.update(color='black', penwidth='0.2')
    for n in range(verts):
        if n == 0:
            g.node(str(n), label=str(n), color='red')
        else:
            g.node(str(n), label=str(n))
        pass

    for d in el:
        g.edge(str(d[0]), str(d[1]))
        e_cout += 1
        pass

    print(e_cout)
    g.render(filename=out_file, directory=outp, cleanup=False, format='png')
    pass


def main():
    el = edge_list("Output/graphEL2.dat")
    # low_deg, high_deg = high_low_deg(el)
    make_graph(el, [], [], "graphEL2")
    print("DONE")
    pass


main()
