"""
This python script creates a traditional parameter study of a particular parameter
when compating it to it's non-local (or old) version.

0. Toggle Density
1. Hop Density
2. Add Density
3. Delete Density
4. Swap Density
5. Local Toggle Density
6. Local Add Density
7. Local Del Density
8. Null Density
"""

total_number_of_commands = 9
ranges_to_test = 1
max_allotment = 1 / 5
intermediate_tests = 3


def main():
    out = open("ParameterSettings.txt", "w")

    for c in range(total_number_of_commands):
        for y in range(0, intermediate_tests + 1):
            for_c = round(y * max_allotment / intermediate_tests, 5)
            for_rest = round((1.0 - for_c) / (total_number_of_commands - 1), 5)
            for z in range(total_number_of_commands):
                if z == c:
                    out.write(str(for_c))
                else:
                    out.write(str(for_rest))
                if z < total_number_of_commands - 1:
                    out.write("\t")
            out.write("\n")
    out.close()


# Command line calls
main()

# Run line:
# python template.py
