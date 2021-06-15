"""
New way to generate graphs?
"""

from math import floor, sqrt

limit = 1000


def print_lsts(lsts: []):
    """

    :type lsts: list
    """
    with open("out.dat", "w") as f:
        cnt = 0
        for ls in lsts:
            for itm in ls:
                f.write(str(itm) + '\t')
                cnt += 1
                pass
            f.write('\n')
            pass
        pass
    # print(cnt)
    pass


def is_prime(n: int):
    for i in range(2, n):
        if n % i == 0:
            return False
        pass
    return True


def get_primes(li: int):
    ls = []
    for i in range(2, li):
        if is_prime(i):
            ls.append(i)
            pass
        pass
    return ls


def main():
    all_primes = get_primes(limit)
    for num_nodes in range(10, limit, 25):
        primes = []
        for x in all_primes:
            if x > (sqrt(num_nodes)):
                primes.append(x)
                pass
            pass
        adj_lsts = [[] for _ in range(num_nodes)]
        cnt = 0
        for fr in range(num_nodes):
            for jmp in primes:
                chk = fr - jmp
                skip = False
                if chk >= 0:
                    if fr in adj_lsts[chk]:
                        skip = True
                        pass
                    pass
                if not skip:
                    to = (fr + jmp) % num_nodes
                    if to not in adj_lsts[fr]:
                        for _ in range(floor(num_nodes / jmp) - 1):
                            if to not in adj_lsts[fr]:
                                if fr not in adj_lsts[to]:
                                    adj_lsts[fr].append(to)
                                    adj_lsts[to].append(fr)
                                    cnt += 1
                                    pass
                                pass
                            to = (to + jmp) % num_nodes
                            pass
                        pass
                    pass
                pass
            pass
        max_edg = num_nodes * (num_nodes - 1) / 2
        print(str(cnt) + " of " + str(max_edg) + " or " + str(float(cnt / max_edg)))
        # print_lsts(adj_lsts)
        pass
    pass


main()
