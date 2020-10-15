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
command_being_tested = 7
tested_against = 3
skip = [4, 6]  # Swap, Local Del
ranges_to_test = 5
max_allotment = 1 / 2
intermediate_tests = 4


def main():
    out = open("ParameterSettings.txt", "w")
    # No density given to those being tested or skipped
    for z in range(total_number_of_commands):
        spread = round(1.0 / (total_number_of_commands - 2 - len(skip)), 5)
        if z == command_being_tested or z == tested_against or skip.count(z) != 0:
            out.write(str(round(0.0, 5)) + "\t")
        else:
            out.write(str(spread) + "\t")
    out.write("\n")

    for x in range(1, ranges_to_test + 1):
        # What is divided between the two commands being tested
        to_split = round(max_allotment * x / ranges_to_test, 5)
        # What is given to each remaining command
        for_rest = round((1 - to_split) / (total_number_of_commands - 2 - len(skip)), 5)
        for y in range(0, intermediate_tests + 1):
            # What is given to the command being tested and the command being tested against
            first_test = round(to_split * y / intermediate_tests, 5)
            second_test = round(to_split - first_test, 5)
            for z in range(total_number_of_commands):
                if z == command_being_tested:
                    out.write(str(first_test) + "\t")
                elif z == tested_against:
                    out.write(str(second_test) + "\t")
                elif skip.count(z) != 0:
                    out.write(str(round(0.0, 5)) + "\t")
                else:
                    out.write(str(for_rest) + "\t")
            out.write("\n")
    out.close()


# Command line calls
main()

# Run line:
# python template.py
