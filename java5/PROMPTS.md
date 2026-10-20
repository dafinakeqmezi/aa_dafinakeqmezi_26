I have an exercise from Advanced Algorithms (Week 4, Task 1 – Trace). The lecture's code is in JavaScript, but implement everything in Python. Please do the following:

1. Create a file search.py and define the lecture's example data: the text T = "JIM SAW ME IN A BARBERSHOP" and the pattern P = "BARBER".

2. Implement these functions in Python, exactly as the lecture's versions work, keeping the same names. Don't optimize or "fix" them, since the goal is to trace the lecture's code:
   - bruteForce(T, P): place the pattern at each position i from 0 to n - m, compare left to right, return i on a full match, and move one position right on a mismatch. Return -1 if nothing matches.
   - shiftTable(P): a dict storing, for every character of the pattern except the last one, the shift value m - 1 - j (later occurrences overwrite earlier ones).
   - shift(table, c, m): return the table value for character c if it exists, otherwise m.
   - horspool(T, P): i is the text position under the pattern's last character, starting at m - 1. Compare the pattern right to left against the text. On a full match, return i - m + 1. Otherwise, shift i by the value for T[i]. Return -1 if no match.
   - horspool2(T, P): identical to horspool, except the shift is decided by T[i - k], the text character where the mismatch happened, instead of T[i].

3. Inside the while loop of both horspool and horspool2, add print(i - m + 1) as the first line so every alignment is printed.

4. Call all four functions (shiftTable(P), bruteForce(T, P), horspool(T, P), horspool2(T, P)), print the results clearly, and run the file with python.

5. Show me the full output, then briefly explain:
   - what the shift table for "BARBER" contains,
   - which alignments horspool and horspool2 try and how far each one shifts at every step,
   - why using T[i - k] instead of T[i] changes the behavior, and whether horspool2 is always correct or can skip a match,
   - how many alignments bruteForce tries compared with the two Horspool versions.

---

I have the next exercise from Advanced Algorithms (Week 4, Task 2 – Write). The slides ask for JavaScript, but implement everything in Python and continue in the same file. Please do the following:

1. Keep everything in one file, search.py, written by me. Keep the Task 1 functions (bruteForce, shiftTable, shift, horspool, horspool2) in it.

2. Rules for the whole file:
   - Don't use the Python equivalents of indexOf, includes, search, match, replace, split, startsWith, endsWith: no find, index, in on strings, re, replace, split, startswith or endswith.
   - Add a counter comparisons: +1 every time a pattern character is compared with a text character.
   - Add a counter alignments: +1 every time the pattern is placed against the text.
   - resetCounters() sets both counters to 0, and getCounters() returns {"comparisons": ..., "alignments": ...}.
   - The file must end with this export, in this order:
     __all__ = [
         "bruteForce", "shiftTable", "horspool", "horspool2",
         "findAll", "highlight", "goodSuffixTable", "boyerMoore", "resetCounters", "getCounters",
     ]

3. Implement these functions in Python, keeping the lecture's names and following its steps exactly:
   - findAll(T, P): start from horspool. Do alignments += 1 each time round the outer loop and comparisons += 1 before every character comparison. On a full match, save i - m + 1 and keep going. After a match, shift exactly as after a mismatch, by the table value of T[i]. Return the start of every match in order, count overlapping matches, and return [] if there is no match.
   - highlight(T, P): get the matches with findAll, walk through the text and build a new string character by character, put [ before and ] after every match, and skip a match that starts inside the previous highlighted one. Return a new string, without using replace or split. If there is no match, the text comes back unchanged.
   - goodSuffixTable(P): for each k = 1 … m - 1 (the suffix is the last k characters), look to the left for the rightmost other copy of the suffix that is not preceded by the same character as the suffix; a copy at the very start of the pattern counts. If it is found, d2[k] is the distance between that copy and the suffix. If not, take the longest prefix of size l < k that equals the suffix of size l, and set d2[k] = m - l (m if there is none). Return a list of length m with d2[0] = 0. It must work for any characters.
   - boyerMoore(T, P): t1 = shiftTable(P), d2 = goodSuffixTable(P). Compare from right to left as in horspool, where k is the number of characters matched. On a full match, return i - m + 1. On a mismatch, c = T[i - k] is the text character that failed, and d1 = max(t1(c) - k, 1). Shift by d1 if k = 0, otherwise by max(d1, d2[k]). Return the first match, or -1. Use the counters as in findAll.

4. Check every function against the lecture's examples:
   kur = "Kur ngjite përpjetë, shiko dhe tatëpjetë."
   - findAll(kur, "pjetë") → [14, 35], with counters 20 comparisons, 10 alignments
   - findAll("banana", "ana") → [1, 3]
   - highlight(kur, "pjetë") → "Kur ngjite për[pjetë], shiko dhe tatë[pjetë]."
   - highlight("banana", "ana") → "b[ana]na"
   - goodSuffixTable("ABCBAB") → [0, 2, 4, 4, 4, 4]
   - goodSuffixTable("BAOBAB") → [0, 2, 5, 5, 5, 5]
   - goodSuffixTable("tatëpjetë") → [0, 9, 5, 9, 9, 9, 9, 9, 9]
   - boyerMoore("BESS KNEW ABOUT BAOBABS", "BAOBAB") → 16, with counters 12 comparisons, 4 alignments
   - boyerMoore("Shqiptari me armë e shokë, s'i lutet kurkujt mbi tokë.", "tokë") → 49

5. Run the checks with python, show me the full output, and tell me if any result is different from the expected one.
