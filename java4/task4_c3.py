
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


def c3(a, key, lo, hi, trace=False):
    d = [0] * (hi - lo + 1)
    for i in range(len(a)):  
        d[key(a[i]) - lo] += 1
    if trace:
        print("D after count:", d)
    for j in range(1, len(d)):  
        d[j] += d[j - 1]
    if trace:
        print("D after sums: ", d)
        print()
    s = [None] * len(a)
    for i in range(len(a)):  
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        if trace:
            print(f"i={i}  {a[i]['name']:<7} key={key(a[i])}  j={j}  -> S[{d[j] - 1}]")
        d[j] -= 1
    return s


if __name__ == "__main__":
    s = c3(six, g, 5, 10, trace=True)
    print()
    print("S =", " ".join(f"{r['name']}({r['grade']})" for r in s))
