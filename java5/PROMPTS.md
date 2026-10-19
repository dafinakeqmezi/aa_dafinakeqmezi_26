I have an exercise from Advanced Algorithms (Week 4, Task 1 – Trace). Please do the following:

1. Create a file search.js and define the lecture's example data: the text T = "JIM SAW ME IN A BARBERSHOP" and the pattern P = "BARBER".

2. Implement these functions in JavaScript, exactly as the lecture's versions work. Don't optimize or "fix" them, since the goal is to trace the lecture's code:
   - bruteForce(T, P): place the pattern at each position i from 0 to n - m, compare left to right, return i on a full match, and move one position right on a mismatch. Return -1 if nothing matches.
   - shiftTable(P): a Map storing, for every character of the pattern except the last one, the shift value m - 1 - j (later occurrences overwrite earlier ones).
   - shift(table, c, m): return the table value for character c if it exists, otherwise m.
   - horspool(T, P): i is the text position under the pattern's last character, starting at m - 1. Compare the pattern right to left against the text. On a full match, return i - m + 1. Otherwise, shift i by the value for T[i]. Return -1 if no match.
   - horspool2(T, P): identical to horspool, except the shift is decided by T[i - k], the text character where the mismatch happened, instead of T[i].

3. Inside the while loop of both horspool and horspool2, add console.log(i - m + 1) as the first line so every alignment is printed.

4. Call all four functions (shiftTable(P), bruteForce(T, P), horspool(T, P), horspool2(T, P)), print the results clearly, and run the file with node.

5. Show me the full output, then briefly explain:
   - what the shift table for "BARBER" contains,
   - which alignments horspool and horspool2 try and how far each one shifts at every step,
   - why using T[i - k] instead of T[i] changes the behavior, and whether horspool2 is always correct or can skip a match,
   - how many alignments bruteForce tries compared with the two Horspool versions.