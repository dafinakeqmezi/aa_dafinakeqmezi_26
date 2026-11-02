# Week 5 - Task 2: Write (checks against the slides' expected results)

from hashing import (
    W, DELETED, probeInsert, probeFind, remove, doubleHashInsert, doubleHashFind,
    maxComparisons, insertGrow,
)


def build():
    T = [None] * 13
    for w in W:
        probeInsert(T, w)
    return T


def check(call, real, expected):
    ok = "yes" if real == expected else "NO"
    if len(str(expected)) > 15:
        print(f"{call:<60}{ok}\n  expected {expected}\n  real     {real}")
    else:
        print(f"{call:<28}{str(expected):<16}{str(real):<16}{ok}")


if __name__ == "__main__":
    print(f"{'call':<28}{'expected':<16}{'real':<16}match")

    # remove: table built again as on slide 1
    T = build()
    check("remove(T, 'ARE')", remove(T, "ARE"), 11)
    check("probeFind(T, 'SOON')", probeFind(T, "SOON"), 12)
    check("probeFind(T, 'ARE')", probeFind(T, "ARE"), -1)
    check("remove(T, 'KID')", remove(T, "KID"), -1)
    check("len(T)", len(T), 13)
    print("T after remove:", T)
    print()

    # double hashing: the lecture's numbers
    N = [30, 20, 56, 75, 31, 19]
    D = [None] * 11
    for k in N:
        doubleHashInsert(D, k)
    check("D", D, [None, 56, None, 31, 75, 19, None, None, 30, 20, None])
    check("doubleHashFind(D, 19)", doubleHashFind(D, 19), 5)
    check("doubleHashFind(D, 42)", doubleHashFind(D, 42), -1)
    print()

    # maxComparisons: keys must not be changed
    N_before, W_before = list(N), list(W)
    check("maxComparisons(N, 11)", maxComparisons(N, 11), {"chained": 3, "linear": 6, "double": 2})
    check("maxComparisons(W, 13)", maxComparisons(W, 13), {"chained": 2, "linear": 2, "double": 3})
    check("N, W unchanged", N == N_before and W == W_before, True)
    print()

    # insertGrow: start from 5 cells, record the size after every insert
    G = [None] * 5
    sizes = []
    for w in W:
        G = insertGrow(G, w)
        sizes.append(len(G))
    check("sizes", sizes, [5, 5, 11, 11, 11, 23, 23, 23])
    check("len(G)", len(G), 23)
    check("probeFind(G, 'ARE')", probeFind(G, "ARE"), 4)
    print("G:", G)

    # same table back when it does not grow, no DELETED in a new table
    S = [None] * 11
    check("same table if no grow", insertGrow(S, "A") is S, True)
    R = [None] * 5
    for w in ["A", "FOOL"]:
        R = insertGrow(R, w)
    remove(R, "A")
    R = insertGrow(R, "AND")
    R = insertGrow(R, "HIS")  # n = 2, (2 + 1) / 5 > 0.5 -> grows, drops DELETED
    check("no DELETED after grow", DELETED in R, False)
    check("len(R)", len(R), 11)
