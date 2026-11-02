# Week 5 - Task 1: Trace (predicted vs real, calls run in the slide's order)

from hashing import W, T, h, chainedTable, probeFind, probeRemove

# Predicted on paper from the slides' code, before running: h = sum of
# letters (A=1..Z=26) mod 13, linear probing puts SOON at 12 and PARTED wraps
# around to 0. probeRemove empties cell 11 (sets it to null), so the search
# for SOON stops there and never reaches cell 12.
predicted = {
    "chainedTable(W, 13)[11]": "['ARE', 'SOON']",
    "probeFind(T, 'PARTED')": "0",
    "probeFind(T, 'KID')": "-1",
    "probeRemove(T, 'ARE')": "11",
    "probeFind(T, 'SOON')": "-1",
}

if __name__ == "__main__":
    print("hashes:", {w: h(w, 13) for w in W + ["KID"]})
    print("T after inserts:", T)
    print()

    real = {}
    real["chainedTable(W, 13)[11]"] = str(chainedTable(W, 13)[11])
    real["probeFind(T, 'PARTED')"] = str(probeFind(T, "PARTED"))
    real["probeFind(T, 'KID')"] = str(probeFind(T, "KID"))
    print("probe path for 'KID' before the remove (slot, content):")
    probeFind(T, "KID", trace=True)
    print()
    real["probeRemove(T, 'ARE')"] = str(probeRemove(T, "ARE"))
    real["probeFind(T, 'SOON')"] = str(probeFind(T, "SOON"))

    print(f"{'call':<26}{'predicted':<18}{'real':<18}match")
    for call in predicted:
        ok = "yes" if predicted[call] == real[call] else "NO"
        print(f"{call:<26}{predicted[call]:<18}{real[call]:<18}{ok}")

    print("\nT after remove:", T)
    print("\nprobe path for 'SOON' after the remove (slot, content):")
    probeFind(T, "SOON", trace=True)
