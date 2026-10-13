
from counting import (
    six, g, recs, words,
    comparisonCountingSort, distributionCountingSort, sortByDate,
    tokenize, sortAlbanian, resetCounters, getCounters,
)


def names(rs):
    return " ".join(r["name"] for r in rs)


print("comparisonCountingSort")
resetCounters()
print("  comparisonCountingSort(six, g)    ->", names(comparisonCountingSort(six, g)))
print("  comparisons after one call on six ->", getCounters()["comparisons"])

print("\ndistributionCountingSort")
resetCounters()
print("  distributionCountingSort(six, g, 5, 10) ->", names(distributionCountingSort(six, g, 5, 10)))
print("  distributionCountingSort([1003, 1001, 1002, 1001], x => x, 1001, 1003)")
print("    ->", distributionCountingSort([1003, 1001, 1002, 1001], lambda x: x, 1001, 1003))
print("  counters ->", getCounters())

print("\nsortByDate")
resetCounters()
print("  sortByDate(recs).map(r => r.id) ->", " ".join(str(r["id"]) for r in sortByDate(recs)))
print("  counters ->", getCounters())

print("\ntokenize / sortAlbanian")
print("  tokenize('llamba') ->", tokenize("llamba"))
print("  tokenize('shtëpi') ->", tokenize("shtëpi"))
resetCounters()
print("  sortAlbanian(words) ->", " ".join(sortAlbanian(words)))
print("  counters ->", getCounters())
