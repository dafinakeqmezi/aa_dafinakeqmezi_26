T = "JIM SAW ME IN A BARBERSHOP"
P = "BARBER"


comparisons = 0  
alignments = 0  


def resetCounters():
    global comparisons, alignments
    comparisons = 0
    alignments = 0


def getCounters():
    return {"comparisons": comparisons, "alignments": alignments}


def same(p, t):
    global comparisons
    comparisons += 1
    return p == t


def place():
    global alignments
    alignments += 1


def bruteForce(T, P):
    n, m = len(T), len(P)
    for i in range(n - m + 1):
        place()
        j = 0
        while j < m and same(P[j], T[i + j]):
            j += 1
        if j == m:
            return i
    return -1


def shiftTable(P):
    m = len(P)
    table = {}
    for j in range(m - 1):
        table[P[j]] = m - 1 - j
    return table


def shift(table, c, m):
    return table[c] if c in table else m


def horspool(T, P, trace=False):
    n, m = len(T), len(P)
    table = shiftTable(P)
    i = m - 1
    while i <= n - 1:
        if trace:
            print(i - m + 1)
        place()
        k = 0
        while k <= m - 1 and same(P[m - 1 - k], T[i - k]):
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i], m)
    return -1


def horspool2(T, P, trace=False):
    n, m = len(T), len(P)
    table = shiftTable(P)
    i = m - 1
    while i <= n - 1:
        if trace:
            print(i - m + 1)
        place()
        k = 0
        while k <= m - 1 and same(P[m - 1 - k], T[i - k]):
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i - k], m)
    return -1



def findAll(T, P):
    n, m = len(T), len(P)
    found = []
    if m == 0:
        return found
    table = shiftTable(P)
    i = m - 1
    while i <= n - 1:
        place()
        k = 0
        while k <= m - 1 and same(P[m - 1 - k], T[i - k]):
            k += 1
        if k == m:
            found.append(i - m + 1)
        i += shift(table, T[i], m)
    return found


def highlight(T, P):
    m = len(P)
    starts = findAll(T, P)
    out = ""
    s = 0
    end = -1
    for i in range(len(T)):
        if s < len(starts) and starts[s] == i:
            s += 1
            if i > end:
                out += "["
                end = i + m - 1
        out += T[i]
        if i == end:
            out += "]"
    return out



def goodSuffixTable(P):
    m = len(P)
    d2 = [0] * m
    for k in range(1, m):
        d = 0
        for s in range(m - k - 1, -1, -1):
            j = 0
            while j < k and P[s + j] == P[m - k + j]:
                j += 1
            if j == k and (s == 0 or P[s - 1] != P[m - k - 1]):
                d = m - k - s
                break
        if d == 0:
            d = m
            for l in range(k - 1, 0, -1):
                j = 0
                while j < l and P[j] == P[m - l + j]:
                    j += 1
                if j == l:
                    d = m - l
                    break
        d2[k] = d
    return d2

def boyerMoore(T, P):
    n, m = len(T), len(P)
    t1, d2 = shiftTable(P), goodSuffixTable(P)
    i = m - 1
    while i <= n - 1:
        place()
        k = 0
        while k <= m - 1 and same(P[m - 1 - k], T[i - k]):
            k += 1
        if k == m:
            return i - m + 1
        c = T[i - k]
        d1 = max(shift(t1, c, m) - k, 1)
        i += d1 if k == 0 else max(d1, d2[k])
    return -1


__all__ = [
    "bruteForce", "shiftTable", "horspool", "horspool2",
    "findAll", "highlight", "goodSuffixTable", "boyerMoore", "resetCounters", "getCounters",
]
