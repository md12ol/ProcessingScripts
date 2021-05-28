"""
Makes the edge data (linked list rep) file to create the graph visualizations.
"""


def main():
    filename = "./Input/Graph0.dat"
    edges = 0
    nodes = 128
    data = [[] for i in range(nodes)]
    with open(filename) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for line in lines:
            line = line.rstrip()
            words = line.split(" ")
            data[int(words[0])].append(int(words[1]))
            data[int(words[1])].append(int(words[0]))
            edges += 1
            pass
        pass
    with open("./Output/EdgeList.dat", "w") as f:
        f.write(str(nodes) + '\t' + str(edges) + '\n')
        for idx,list in enumerate(data):
            for n in list:
                f.write(str(idx) + "\t" + str(n) + "\n")
            f.write("\n")
            pass
        pass
    pass


main()
