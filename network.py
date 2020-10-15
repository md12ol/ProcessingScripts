from graphviz import Graph

"""
Generates the graph visual
"""

inp = "./Input/"
exp_str = "SIR"
prof_count = 9
exp_count = 8


def loadData(fName):
    data = []
    with open(fName) as f:
        # This is just a nifty python thing that lets us avoid exceptions
        lines = f.readlines()  # Reads every line into a list
        samp = 0
        for line in lines:
            data.append(line.split())
    return data


def main():
    g = Graph('G', filename='graph.gv', engine='sfdp')
    data = loadData(inp + exp_str + 'graphP' + str(1) + 'E' + str(1) + '.txt')

    g.edge(data[0][0], data[0][1])

    g.view()

    # g.save()
    pass


main()
