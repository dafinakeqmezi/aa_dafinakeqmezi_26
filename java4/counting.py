# Week 3 - Counting sorts (Task 1: Trace, Task 2: Write)

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


recs = [
    {"id": 0, "date": "2024-10-13"}, {"id": 1, "date": "2024-01-20"}, {"id": 2, "date": "2026-05-15"},
    {"id": 3, "date": "2024-01-15"}, {"id": 4, "date": "2024-05-02"}, {"id": 5, "date": "2026-08-27"},
    {"id": 6, "date": "2025-02-19"}, {"id": 7, "date": "2026-11-22"}, {"id": 8, "date": "2024-09-10"},
    {"id": 9, "date": "2026-12-11"},
]


# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------

comparisons = 0  # +1 every time two keys are compared
passes = 0  # +1 for every counting pass (count -> running sums -> place)


def resetCounters():
    global comparisons, passes
    comparisons = 0
    passes = 0


def getCounters():
    return {"comparisons": comparisons, "passes": passes}


# ---------------------------------------------------------------------------
# Task 1: c1, c2, c3 exactly as on the slides
# ---------------------------------------------------------------------------

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

def c2(a, key, lo, hi):
    d = [0] * (hi - lo + 1)
    for i in range(len(a)):  
        d[key(a[i]) - lo] += 1
    for j in range(1, len(d)):  
        d[j] += d[j - 1]
    s = [None] * len(a)
    for i in range(len(a) - 1, -1, -1):  
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        d[j] -= 1
    return s


def c3(a, key, lo, hi):
    d = [0] * (hi - lo + 1)
    for i in range(len(a)): 
        d[key(a[i]) - lo] += 1
    for j in range(1, len(d)): 
        d[j] += d[j - 1]
    s = [None] * len(a)
    for i in range(len(a)):  
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        d[j] -= 1
    return s


# ---------------------------------------------------------------------------
# Task 2: counted, stable versions
# ---------------------------------------------------------------------------

def comparisonCountingSort(a, key):
    global comparisons
    n = len(a)
    count = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            if key(a[i]) <= key(a[j]):
                count[j] += 1
            else:
                count[i] += 1
    s = [None] * n
    for i in range(n):
        s[count[i]] = a[i]
    return s

def distributionCountingSort(a, key, lo, hi):
    global passes
    passes += 1  
    d = [0] * (hi - lo + 1)
    for i in range(len(a)): 
        d[key(a[i]) - lo] += 1
    for j in range(1, len(d)):  
        d[j] += d[j - 1]
    s = [None] * len(a)
    for i in range(len(a) - 1, -1, -1):  
        j = key(a[i]) - lo
        s[d[j] - 1] = a[i]
        d[j] -= 1
    return s


def year(r):
    return int(r["date"][0:4])


def month(r):
    return int(r["date"][5:7])


def day(r):
    return int(r["date"][8:10])


def sortByDate(records):
    lo = hi = year(records[0]) if records else 0  
    for r in records:
        if year(r) < lo:
            lo = year(r)
        if year(r) > hi:
            hi = year(r)
    s = distributionCountingSort(records, day, 1, 31)  
    s = distributionCountingSort(s, month, 1, 12)  
    return distributionCountingSort(s, year, lo, hi)  


# The Albanian alphabet, 1..36.
ALPHABET = [
    "a", "b", "c", "ç", "d", "dh", "e", "ë", "f", "g", "gj", "h",
    "i", "j", "k", "l", "ll", "m", "n", "nj", "o", "p", "q", "r",
    "rr", "s", "sh", "t", "th", "u", "v", "x", "xh", "y", "z", "zh",
]
NUMBER = {letter: i + 1 for i, letter in enumerate(ALPHABET)}  # a = 1 ... zh = 36
DOUBLE = {"dh", "gj", "ll", "nj", "rr", "sh", "th", "xh", "zh"}

words = [
    "shi", "çaj", "llamba", "zemër", "dhe", "gur", "nënë", "tokë", "xhami", "emër",
    "rrugë", "cep", "ëndërr", "drita", "thikë", "lule", "njeri", "gjak", "zhurmë",
    "rosa", "dera", "sot", "xixa", "dhelpër",
]


# Reads the word left to right. If the next two characters are one of
# dh gj ll nj rr sh th xh zh, they are one letter. Returns the letter numbers.
def tokenize(word):
    letters = []
    i = 0
    while i < len(word):
        if word[i:i + 2] in DOUBLE:
            letters.append(NUMBER[word[i:i + 2]])
            i += 2
        else:
            letters.append(NUMBER[word[i]])
            i += 1
    return letters


# Dictionary order: one distributionCountingSort per letter position, last
# position first, range 0..36. A word with no letter at that position gets 0,
# so a shorter word comes before a longer word that starts the same way.
def sortAlbanian(words):
    tokens = [tokenize(w) for w in words]  # 2. tokenize every word
    longest = 0  # 2. find the longest one
    for t in tokens:
        if len(t) > longest:
            longest = len(t)
    order = list(range(len(words)))
    for p in range(longest - 1, -1, -1):  # 3. last position first
        order = distributionCountingSort(
            order, lambda i: tokens[i][p] if p < len(tokens[i]) else 0, 0, 36
        )
    return [words[i] for i in order]


__all__ = [
    "c1", "c2", "c3", "comparisonCountingSort", "distributionCountingSort",
    "sortByDate", "tokenize", "sortAlbanian", "resetCounters", "getCounters",
]
