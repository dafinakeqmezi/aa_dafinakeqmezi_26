from search import findAll, highlight, goodSuffixTable, boyerMoore, resetCounters, getCounters

kur = "Kur ngjite përpjetë, shiko dhe tatëpjetë."

print("findAll")
resetCounters()
print("  findAll(kur, 'pjetë')    ->", findAll(kur, "pjetë"), "  counters ->", getCounters())
print("  findAll('banana', 'ana') ->", findAll("banana", "ana"))

print("\nhighlight")
print("  highlight(kur, 'pjetë')    ->", repr(highlight(kur, "pjetë")))
print("  highlight('banana', 'ana') ->", repr(highlight("banana", "ana")))

print("\ngoodSuffixTable")
print("  goodSuffixTable('ABCBAB')    ->", goodSuffixTable("ABCBAB"))
print("  goodSuffixTable('BAOBAB')    ->", goodSuffixTable("BAOBAB"))
print("  goodSuffixTable('tatëpjetë') ->", goodSuffixTable("tatëpjetë"))

print("\nboyerMoore")
resetCounters()
print("  boyerMoore('BESS KNEW ABOUT BAOBABS', 'BAOBAB') ->",
      boyerMoore("BESS KNEW ABOUT BAOBABS", "BAOBAB"), "  counters ->", getCounters())
print("  boyerMoore(\"Shqiptari me armë e shokë, s'i lutet kurkujt mbi tokë.\", 'tokë') ->",
      boyerMoore("Shqiptari me armë e shokë, s'i lutet kurkujt mbi tokë.", "tokë"))
