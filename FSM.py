import random

from graphviz import Graph

states = 5
edges = [[1, 2], [4, 3], [4, 2], [0, 1], [3, 0]]


def main():
    random.seed(5321)
    f = Graph(engine="dot")
    f.graph_attr.update(dpi="600", size="3,3", overlap="false", splines="true", rankdir="LR")
    f.node_attr.update(shape="circle", fixedsize='true', height="0.5", width="0.5")
    f.edge_attr.update(dir="forward", aarowhead="normal", arrowsize="0.75", minlen="1")

    for n in range(states):
        s = random.randint(1, 2)
        b = ""
        for _ in range(s):
            b += str(random.randint(0, 1))
        f.node(str(n), label=b)
        pass

    f.node(str(states), label="", shape="none", height="0.0", width="0.0")
    f.edge(str(states), "0")

    for n in range(states):
        for i in range(2):
            f.edge(str(n), str(edges[n][i]), label=str(" " + str(i)))
            pass
        pass

    f.render(filename="FSM", directory="./Output/", cleanup=True, format="png")
    pass


main()
