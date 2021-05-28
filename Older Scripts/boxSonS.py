import math
import sys

import matplotlib.pyplot as plt  # This is the plotting one
import numpy as np

"""
This script makes a fitness plot with 95% CI of the fitness (numerical) vs 
parameter setting for several experiments on one plot
"""

num_expts = 4
samps = 0


def loadData(fName, tests, samples):
    with open(fName) as f:
        lines = f.readlines()  # Reads every line into a list
        data = [[] for i in range(tests)]
        imp_data = []
        # Grab data from the lines but cast it into a float
        line = lines[1]
        line = line.split()
        li = []
        for l in line:
            li.append(int(float(l)))
        imp_data.append(li)

        line = lines[3]
        line = line.split()
        li = []
        for l in line:
            li.append(int(float(l)))
        imp_data.append(li)

        line = lines[5]
        line = line.split()
        li = []
        for l in line:
            li.append(int(float(l)))
        imp_data.append(li)

        line = lines[7]
        line = line.split()
        li = []
        for l in line:
            li.append(int(float(l)))
        imp_data.append(li)
        return data, imp_data  # Returns as a 2d array


def pop_zeros(items):
    while items[-1] == 0:
        items.pop()
        pass
    pass


def get_prof(fname):
    with open(fname) as f:
        lines = f.readlines()  # Reads every line into a list
        data = []
        for line in lines:  # For each experiment...
            data.append(int(line))
    return data


def add_zeros(li, num):
    for x in range(len(li), num):
        li.append(0)
    pass


def main():
    for ps in range(1,10):
        epi_in = "./Input/SonSProfile" + str(ps) + ".dat"
        prof_in = "./Profiles/Profile" + str(ps) + ".dat"
        data, sums = loadData(epi_in, num_expts, samps)

        list(map(list, zip(*data)))
        for i in range(num_expts):
            # sums[i][:] = [x / 50.0 for x in sums[i]]
            pop_zeros(sums[i])
            pass

        prof = get_prof(prof_in)
        print("hey")
        pop_zeros(prof)
        length = max(max(len(sums[x]) for x in range(num_expts)), 16)
        add_zeros(prof, length)
        for li in sums:
            add_zeros(li, length)
            pass

        order = []
        for v in sums:
            order.append(v[0])
            pass

        xs = [x for x in range(length)]

        plt.rc('xtick', labelsize=7)
        plt.rc('ytick', labelsize=7)

        fig = plt.figure()
        plt.plot(xs, prof, label='Original Profile')
        plt.plot(xs, sums[0], label='SIR under SIR epidemic')
        plt.plot(xs, sums[1], label='SIR under SIIR epidemic')
        plt.plot(xs, sums[2], label='SIIR under SIR epidemic')
        plt.plot(xs, sums[3], label='SIIR under SIIR epidemic')

        plt.legend()

        plt.tight_layout(0.5, 0.5, 0)
        fig.savefig('./Output/SonS' + str(ps) + '.png')


# Command line calls
main()

# Run line:
# python boxSonS.py
