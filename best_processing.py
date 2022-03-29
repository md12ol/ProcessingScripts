"""
This script will take in a best.lint file which contains the best output from each run of an evolutionary algorithm.
Each run contains: best fitness, gene, and graph
It will output one file
"""
from operator import itemgetter

runs = 30
lower_better = True
keep_n = 3
finame = "best.lint"
inp = "./Input/"
outp = "./Output/"


def get_data(dir_path: str):
    fits = []
    graph = []
    graphs = []

    with open(dir_path + finame) as f:
        lines = f.readlines()
        next_graph = False
        for line in lines:
            if line.__contains__(str("-fitness")):
                d = line.split(" ")
                fits.append(float(d[0]))
                next_graph = False
                graphs.append(graph)
                graph = []
                pass
            elif line.__contains__(str("Graph")):
                next_graph = True
                pass
            elif next_graph:
                graph.append(line)
                pass
            pass
        pass
    data = [[i, fits[i], graphs[i]] for i in range(runs)]
    data.sort(key=itemgetter(1))  # Ascending
    if not lower_better:
        data.reverse()
        pass
    return data


def main():
    print("START")
    sizes = [256, 512, 768, 1024]
    data = []

    for si in sizes:
        fold = inp + "Output - P1 w " + str(si) + "N/"
        data.append(get_data(fold))
        pass

    for idx, si in enumerate(sizes):
        out_root = outp + str(si) + "N_graph"
        for g in range(keep_n):
            output = out_root + "Run" + str(data[idx][g][0]) + "_" + str(g + 1) + "Place.dat"
            print(data[idx][g][0])
            with open(output, "w") as f:
                for line in data[idx][g][2]:
                    f.write(line)
                    pass
                pass
            pass
        pass
    print("DONE")
    pass


main()
