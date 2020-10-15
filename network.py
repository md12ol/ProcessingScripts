from graphviz import Graph

inp = "./Input/"
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


def makeGraph():
    exp_strs = ['SIR', 'SIIR']
    for exp_str in exp_strs:
        for prof in range(1, prof_count + 1):
            for exp in range(1, exp_count + 1):
                outName = exp_str + 'graphP' + str(prof) + 'E' + str(exp)
                g = Graph(engine='sfdp')
                data = loadData(inp + exp_str + 'graphP' + str(prof) + 'E' + str(exp) + '.txt')
                g.attr(overlap='false')
                g.node_attr.update(fixedsize='true', fontsize='12', width='0.5', height='0.5', style='filled')

                g.node_attr.update(fillcolor='red')
                g.node('0')
                for n in range(1,32):
                    g.node(str(n), fillcolor='cyan')

                for n in range(32,64):
                    g.node(str(n), fillcolor='orange')

                for n in range(64,96):
                    g.node(str(n), fillcolor='yellow')

                for n in range(96,128):
                    g.node(str(n), fillcolor='green')

                for d in data:
                    if d[0] >= d[1]:
                        g.edge(d[0], d[1], weight=0.5)

                g.render(filename=outName, directory='Output/' + str(exp_str) + '/Profile ' + str(prof), cleanup=True,
                         format='png')



def main():
    makeGraph()
    pass


main()

