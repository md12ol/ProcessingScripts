"""
Makes the edge data (linked list rep) file to create the graph
"""


def main():
    filename = "./Input/musae_git_edges.csv"
    edges = 0
    nodes = 37700
    data = [[] for i in range(nodes)]
    with open(filename) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for line in lines:
            line = line.rstrip()
            words = line.split(",")
            data[int(words[0])].append(int(words[1]))
            data[int(words[1])].append(int(words[0]))
            edges += 1
    with open("./Output/github.dat", "w") as f:
        f.write(str(nodes) + '\t' + str(edges) + '\n')
        for idx,list in enumerate(data):
            f.write(str(idx) + "\t")
            for n in list:
                f.write(str(n) + "\t")
            f.write("\n")
    pass


main()
