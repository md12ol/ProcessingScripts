import os
import re

fin = "./Input/"
rex = "run+\\d+\\.dat"


def make_best(path: str, out: str):
    fits = []
    for root, dir, files in os.walk(path):
        for file in files:
            if re.match(rex, file):
                to_add = [root + "/" + file]
                with open(root + "/" + file) as o:
                    lines = o.readlines()
                    lline = lines[-1]
                    words = lline.split(" ")
                    to_add.append(words[-1].replace("\n", ""))
                    pass
                fits.append(to_add)
                pass
            pass
        pass
    with open(out, "w") as o:
        b_idx = 0
        b_fit = 0
        for idx, fit in enumerate(fits):
            o.write(str(fit[0]) + " " + str(fit[1]) + " -fitnessEL\n")
            if float(fit[1]) > b_fit:
                b_fit = float(fit[1])
                b_idx = idx
            pass
        pass
        o.write("Best: " + str(fits[b_idx][0]) + " " + str(fits[b_idx][1]))
    pass


def main():
    for dir in os.listdir(fin):
        make_best(fin + dir, fin + dir + "/best.lint")
    pass


main()
