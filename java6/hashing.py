W = ["A", "FOOL", "AND", "HIS", "MONEY", "ARE", "SOON", "PARTED"]


class _Deleted:
    def __repr__(self):
        return "Symbol(deleted)"


DELETED = _Deleted()  # like Symbol('deleted'): unique, equal only to itself


def num(key):
    if isinstance(key, int):
        return key
    s = 0
    for c in key:
        s += ord(c) - 64
    return s


def h(key, m):
    return num(key) % m


def chainedTable(keys, m):
    table = []
    for i in range(m):
        table.append([])
    for k in keys:
        table[h(k, m)].append(k)
    return table


def probeInsert(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        i = (i + 1) % m
    table[i] = key
    return i


def probeFind(table, key, trace=False):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if trace:
            print(i, table[i])
        if table[i] == key:
            return i
        i = (i + 1) % m
    if trace:
        print(i, table[i])
    return -1


def probeRemove(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = None
            return i
        i = (i + 1) % m
    return -1


def remove(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = DELETED
            return i
        i = (i + 1) % m
    return -1


def doubleHashInsert(table, key):
    m = len(table)
    i = h(key, m)
    s = m - 2 - num(key) % (m - 2)
    while table[i] is not None:
        i = (i + s) % m
    table[i] = key
    return i


def doubleHashFind(table, key):
    m = len(table)
    i = h(key, m)
    s = m - 2 - num(key) % (m - 2)
    while table[i] is not None:
        if table[i] == key:
            return i
        i = (i + s) % m
    return -1


def maxComparisons(keys, m):
    chained = chainedTable(keys, m)
    linear = [None] * m
    double = [None] * m
    for k in keys:
        probeInsert(linear, k)
        doubleHashInsert(double, k)

    longest = 0
    for lst in chained:
        if len(lst) > longest:
            longest = len(lst)

    maxLinear = 0
    maxDouble = 0
    for k in keys:
        # linear: count cells from h(k, m) up to and including k's own cell
        i = h(k, m)
        count = 1
        while linear[i] != k:
            i = (i + 1) % m
            count += 1
        if count > maxLinear:
            maxLinear = count

        # double: same walk, with step s
        i = h(k, m)
        s = m - 2 - num(k) % (m - 2)
        count = 1
        while double[i] != k:
            i = (i + s) % m
            count += 1
        if count > maxDouble:
            maxDouble = count

    return {"chained": longest, "linear": maxLinear, "double": maxDouble}


def isPrime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def nextPrime(n):
    # smallest prime >= n
    while not isPrime(n):
        n += 1
    return n


def insertGrow(table, key):
    m = len(table)
    n = 0
    for cell in table:
        if cell is not None and cell is not DELETED:
            n += 1
    if (n + 1) / m > 0.5:
        bigger = [None] * nextPrime(2 * m)
        for cell in table:
            if cell is not None and cell is not DELETED:
                probeInsert(bigger, cell)
        table = bigger
    probeInsert(table, key)
    return table


T = [None] * 13
for w in W:
    probeInsert(T, w)

__all__ = [
    "num", "h", "chainedTable", "probeInsert", "probeFind", "probeRemove",
    "DELETED", "remove", "doubleHashInsert", "doubleHashFind", "maxComparisons", "insertGrow",
]
