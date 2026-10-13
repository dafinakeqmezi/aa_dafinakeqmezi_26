# Week 3 - Task 1: Trace (counting sort on records)

six = [
    {"name": "Arta", "grade": 9},
    {"name": "Blend", "grade": 6},
    {"name": "Dita", "grade": 9},
    {"name": "Edon", "grade": 9},
    {"name": "Fjolla", "grade": 6},
    {"name": "Gent", "grade": 5},
]


def g(r):
    return r["grade"]


# c1: comparison counting sort, as on the lecture slide. count[i] ends up
# as the number of elements that go before a[i], so it is also the position
# where a[i] is written. Each record is moved exactly once.
def c1(a, key):
    n = len(a)
    count = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if key(a[i]) < key(a[j]):
                count[j] += 1
            else:
                count[i] += 1
    s = [None] * n
    for i in range(n):
        s[count[i]] = a[i]
    return s


# c2: distribution counting sort, as on the lecture slide. No two keys are
# ever compared. After the sums, d[j] is one past the last place where key
# lo + j may go.
def c2(a, key, lo, hi):
    d = [0] * (hi - lo + 1)
    for i in range(len(a)):  # count
        d[key(a[i]) - lo] += 1
    for j in range(1, len(d)):  # sums
        d[j] += d[j - 1]
    s = [None] * len(a)
    for i in range(len(a) - 1, -1, -1):  # place
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        d[j] -= 1
    return s


# c3: the same as c2 except the placing loop runs from left to right.
def c3(a, key, lo, hi):
    d = [0] * (hi - lo + 1)
    for i in range(len(a)):  # count
        d[key(a[i]) - lo] += 1
    for j in range(1, len(d)):  # sums
        d[j] += d[j - 1]
    s = [None] * len(a)
    for i in range(len(a)):  # place (left to right)
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        d[j] -= 1
    return s


def show(rs):
    return " ".join(f"{r['name']}({r['grade']})" for r in rs)


if __name__ == "__main__":
    print("c1(six, g)         :", show(c1(six, g)))
    print("c2(six, g, 5, 10)  :", show(c2(six, g, 5, 10)))
    print("c3(six, g, 5, 10)  :", show(c3(six, g, 5, 10)))
