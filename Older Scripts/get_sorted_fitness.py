import re
import sys

"""
This script takes in a file and returns a list of the fitness values sorted in a descending order.
"""


def main(filename, output):
    results = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.__contains__(str("fit")):
                results.append(float(re.findall("\d+\.\d+", line)[0]))
    results.sort()
    with open(output, "w") as f:
        for num in results:
            f.write(str(num) + "\n")
    pass


# Command line call
main(sys.argv[1], sys.argv[2])

# Params
# File of interest
# Output location
# python get_sorted_fitness.py "./Input/lint.best" "./Output/sorted.txt"
