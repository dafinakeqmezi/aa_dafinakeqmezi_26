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


# Predicted before seeing the code of c1, c2 and c3: only the names and
# grades were known, so the grades are sorted 5, 6, 6, 9, 9, 9 and the order
# of equal grades was guessed.
predicted = {
    "c1(six, g)": "Gent Blend Fjolla Arta Dita Edon",
    "c2(six, g, 5, 10)": "Gent Fjolla Blend Edon Dita Arta",
    "c3(six, g, 5, 10)": "Gent Blend Fjolla Arta Dita Edon",
}


def names(rs):
    return " ".join(r["name"] for r in rs)


if __name__ == "__main__":
    real = {
        "c1(six, g)": names(c1(six, g)),
        "c2(six, g, 5, 10)": names(c2(six, g, 5, 10)),
        "c3(six, g, 5, 10)": names(c3(six, g, 5, 10)),
    }
    print(f"{'call':<20}{'predicted order':<36}{'real order':<36}match")
    for call in predicted:
        ok = "yes" if predicted[call] == real[call] else "NO"
        print(f"{call:<20}{predicted[call]:<36}{real[call]:<36}{ok}")
