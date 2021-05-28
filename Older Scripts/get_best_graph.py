import re

"""
Gets the best contact network from one experiment.
"""

inp = "./Input/"
exp_str = "SIIR"
prof_count = 9
exp_count = 8
samps = 30


def loadData(fName):
    data = [[i, 0.0] for i in range(samps)]
    with open(fName) as f:
        # This is just a nifty python thing that lets us avoid exceptions
        lines = f.readlines()  # Reads every line into a list
        samp = 0
        for line in lines:
            if line.__contains__(str("fitness")):
                data[samp][1] = float(re.findall("\d+\.\d+", line)[0])
                samp += 1
    data.sort(key=get_key)
    return data


def get_key(item):
    return item[1]


def to_adj_list(file, out):
    lines = file.readlines()
    lines.pop(0)
    for num, line in enumerate(lines):
        for nbr in line.split():
            out.write(str(num) + '\t' + str(nbr) + '\n')
    pass


def main():
    for prof in range(1, prof_count + 1):  # for each PS
        for exp in range(1, exp_count + 1):
            out = open('./Output/' + str(exp_str) + 'graphP' + str(prof) + 'E' + str(exp) + '.txt', 'w')
            data = loadData(inp + exp_str + str(exp) + "/P" + str(prof) + "/best.lint")
            assert len(data) == samps
            graph = open(inp + exp_str + str(exp) + "/P" + str(prof) + '/Graph' + str(data[0][0]) + '.dat', 'r')
            to_adj_list(graph, out)
            out.close()


# Command line call
main()

# Run line:
# python get_best_graph.py
