import random
from random import randint

from graphviz import Graph

states = 5
states = ['1', '2', '3']
edges = [[1, 1, 2, 2], [0, 2, 2, 2], [0, 0, 0, 1]]
characters = ['A', 'C', 'G', 'T']


def main():
    random.seed(553)
    f = Graph(engine="dot")
    f.graph_attr.update(dpi="600", size="3,3", overlap="false", splines="true", rankdir="LR")
    f.node_attr.update(shape="square", fixedsize='true', height="0.5", width="0.5")
    f.edge_attr.update(dir="forward", aarowhead="normal", arrowsize="0.5", minlen="1")

    for idx, st in enumerate(states):
        f.node(str(idx), label=st)
        pass

    f.node(str(states), label="", shape="none", height="0.0", width="0.0")
    f.edge(str(states), "0", label=str(characters[0]))

    for n in range(len(states)):
        for i in range(len(characters)):
            trans = ""
            for j in range(randint(1, 2)):
                trans += str(characters[randint(0, 3)])
                pass
            f.edge(str(n), str(edges[n][i]), label=str(str(characters[i]) + "/" + trans))
            pass
        pass

    f.render(filename="FSM", directory="./Output/", cleanup=True, format="png")
    pass


main()
