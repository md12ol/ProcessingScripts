def main():
    base = "./GraphSprayer \"./Out/\""
    init_bits = [" 8", " 16"]
    var_chance = [" 0.01"]
    edits = [" 12 20", " 20 28", " 28 36"]
    fitness = [" 0", " 1"]
    alp_cng = [" 0.05", " 0.10", " 0.15"]
    runs = 30
    idx = 0

    for b in init_bits:
        for v in var_chance:
            for e in edits:
                for fit in fitness:
                    for ac in alp_cng:
                        with open("./Output/table" + str(idx) + ".dat", "w") as f:
                            idx += 1
                            for i in range(runs):
                                f.write(base + b + v + e + fit + ac + " " + str(i) + '\n')
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass
    print("DONE")
    pass


main()
