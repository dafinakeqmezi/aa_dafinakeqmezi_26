# Week 4 - String search (Task 1: Trace)

T = "JIM SAW ME IN A BARBERSHOP"
P = "BARBER"


# Brute force, as on the lecture slide: place the pattern at i, compare from
# left to right, and on a mismatch move it one place to the right.
def bruteForce(T, P):
    n, m = len(T), len(P)
    for i in range(n - m + 1):
        j = 0
        while j < m and P[j] == T[i + j]:
            j += 1
        if j == m:
            return i
    return -1


# Horspool, as on the lecture slide. The table holds the shift for every
# character of the pattern except the last one; shift gives m for any other
# character.
def shiftTable(P):
    m = len(P)
    table = {}
    for j in range(m - 1):
        table[P[j]] = m - 1 - j
    return table


def shift(table, c, m):
    return table[c] if c in table else m


# i is the text position under the pattern's last character, and the shift
# is decided by T[i].
def horspool(T, P, trace=False):
    n, m = len(T), len(P)
    table = shiftTable(P)
    i = m - 1
    while i <= n - 1:
        if trace:
            print(i - m + 1)  # step 5: the current alignment
        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i], m)
    return -1


# The same as horspool except the highlighted line: the shift is decided by
# T[i - k], the text character where the mismatch happened.
def horspool2(T, P, trace=False):
    n, m = len(T), len(P)
    table = shiftTable(P)
    i = m - 1
    while i <= n - 1:
        if trace:
            print(i - m + 1)  # step 5: the current alignment
        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1
        if k == m:
            return i - m + 1
        i += shift(table, T[i - k], m)
    return -1


__all__ = ["bruteForce", "shiftTable", "shift", "horspool", "horspool2"]
