# Week 3 - c1: comparison counting sort, as on the lecture slide

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


# count[i] ends up as the number of elements that go before a[i], so it is
# also the position where a[i] is written. Each record is moved exactly once.
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
    return s, count


if __name__ == "__main__":
    s, count = c1(six, g)
    print(f"{'i':<3}{'name':<8}{'grade':<7}count[i]")
    for i, r in enumerate(six):
        print(f"{i:<3}{r['name']:<8}{r['grade']:<7}{count[i]}")
    print()
    print("S =", " ".join(f"{r['name']}({r['grade']})" for r in s))
