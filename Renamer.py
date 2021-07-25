import os
import re

fin = "./Input/"
sfin_root = "exp"
sfin_list = [4, 5, 6, 7]
st_idx = [23, 25, 23, 24]
fout = "./Output/"
rxs = ["Graph+\\d+\\.dat", "run+\\d+\\.dat"]
rplc = ["Graph", "run"]


def main():
    print("Current directory is: %s" % os.getcwd())
    for idx, n in enumerate(sfin_list):
        dir = fin + sfin_root + str(n) + "/"
        for root, d, files in os.walk(dir):
            for ridx, rx in enumerate(rxs):
                id = st_idx[idx]
                for f in files:
                    mtch = re.match(rx, f)
                    if mtch:
                        os.renames(root + f, root + rplc[ridx] + str(id) + ".dat")
                        id += 1
                        pass
                pass
            pass
    pass


pass

main()
