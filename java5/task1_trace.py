# Week 4 - Task 1: Trace (predicted vs real result of each call)

from search import T, P, bruteForce, shiftTable, horspool, horspool2

# Predicted on paper like a student seeing the code for the first time,
# before running anything.
predicted = {
    "shiftTable(P)": "{'B': 5, 'A': 4, 'R': 3, 'E': 1}, others 6",
    "bruteForce(T, P)": "16",
    "horspool(T, P)": "21",
    "horspool2(T, P)": "16",
}

real = {
    "shiftTable(P)": f"{shiftTable(P)}, others {len(P)}",
    "bruteForce(T, P)": str(bruteForce(T, P)),
    "horspool(T, P)": str(horspool(T, P)),
    "horspool2(T, P)": str(horspool2(T, P)),
}

print(f"{'call':<18}{'predicted':<46}{'real':<46}match")
for call in predicted:
    ok = "yes" if predicted[call] == real[call] else "NO"
    print(f"{call:<18}{predicted[call]:<46}{real[call]:<46}{ok}")

print("\nhorspool alignments (i - m + 1):")
horspool(T, P, trace=True)

print("\nhorspool2 alignments (i - m + 1):")
horspool2(T, P, trace=True)
