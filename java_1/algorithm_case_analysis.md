# Week 1: Best, Average, and Worst Case Analysis

This document analyzes three algorithms from the point of view of best-case,
average-case, and worst-case behavior.

The selected algorithms are:

1. Hill Climbing for the N-Queens optimization problem
2. Simplex Algorithm for linear programming
3. Euclidean Algorithm for greatest common divisor (GCD)

## 1. Best Case Known, Average and Worst Case Not Practically Fixed

### Algorithm: Hill Climbing for N-Queens

Hill climbing is a local search algorithm. It starts from an initial state and
repeatedly moves to a neighboring state that improves the objective function.
For N-Queens, the objective is usually to minimize the number of attacking queen
pairs.

### Basic idea

```text
Start with an initial board configuration.
While there is a better neighboring configuration:
    Move to the best neighbor.
If no better neighbor exists:
    Stop.
```

### Best case

The best case happens when the initial board configuration is already a valid
solution, or when the algorithm can reach a solution after only one improving
move.

In that case, the algorithm finishes immediately or almost immediately.

If checking the board costs `O(n^2)`, then the best case can be written as:

```text
Best case: O(n^2)
```

The exact value depends on how the board and conflicts are represented.

### Average case

The average case is difficult to define exactly because hill climbing depends on
many choices:

- the starting board
- the neighbor-generation method
- the heuristic function
- tie-breaking between equal moves
- whether random restart is used
- whether sideways moves are allowed

Because of this, there is no single clean average-case complexity for hill
climbing on N-Queens.

### Worst case

The worst case is also not practically fixed in the same way as sorting or GCD
algorithms. Hill climbing can get stuck in a local maximum, plateau, or cycle,
depending on the implementation.

If the algorithm has no step limit and allows cycling, it may fail to terminate.
If a maximum number of steps or random restarts is added, then the worst case is
bounded by that artificial limit.

Therefore:

```text
Best case: known and easy to identify
Average case: depends strongly on implementation and randomness
Worst case: not naturally fixed unless a step limit is defined
```

## 2. Worst Case Known, Best and Average Case Less Meaningful

### Algorithm: Simplex Algorithm

The Simplex Algorithm is used to solve linear programming problems. It moves
from one vertex of the feasible region to another, improving the objective
function until it reaches an optimal solution.

### Basic idea

```text
Start from an initial feasible vertex.
Choose a pivot variable.
Move to a neighboring vertex that improves the objective.
Repeat until no improving pivot exists.
```

### Worst case

The Simplex Algorithm is famous because its worst-case behavior can be
exponential.

There are specially constructed linear programming examples where simplex visits
an exponential number of vertices before reaching the optimum.

For `n` variables, this can be described as:

```text
Worst case: exponential, often written as O(2^n)
```

This does not mean simplex is slow in most real applications. In practice, it is
usually very efficient.

### Best case

The best case can happen if the starting feasible solution is already optimal,
or if the optimum is reached after very few pivots.

However, this best case is not usually the most important analysis of simplex,
because it depends heavily on the starting solution and pivot rule.

### Average case

The average case is hard to characterize because performance depends on:

- the shape of the feasible region
- the number of constraints
- the number of variables
- the pivot rule
- degeneracy
- the distribution of input instances

Because there is no single natural distribution for all linear programming
problems, average-case analysis is not as simple or universal as worst-case
analysis.

Therefore:

```text
Worst case: known exponential behavior
Best case: possible, but input-dependent and less meaningful
Average case: difficult to characterize generally
```

## 3. Best, Average, and Worst Case All Can Be Analyzed

### Algorithm: Euclidean Algorithm for GCD

The Euclidean Algorithm finds the greatest common divisor of two positive
integers `a` and `b`, where `a >= b`.

It is based on the identity:

```text
gcd(a, b) = gcd(b, a mod b)
```

### Basic idea

```text
while b != 0:
    r = a mod b
    a = b
    b = r
return a
```

### Best case

The best case happens when `b` divides `a` exactly.

Example:

```text
gcd(20, 10)
20 mod 10 = 0
answer = 10
```

Only one modulo operation is needed.

```text
Best case: O(1)
```

### Worst case

The worst case happens when the inputs are consecutive Fibonacci numbers.

Example:

```text
gcd(34, 21)
gcd(21, 13)
gcd(13, 8)
gcd(8, 5)
gcd(5, 3)
gcd(3, 2)
gcd(2, 1)
gcd(1, 0)
```

The number of steps grows logarithmically with the smaller input value.

```text
Worst case: O(log n)
```

where `n` is the smaller of the two input numbers.

### Average case

The average case is also logarithmic. For typical pairs of integers, the number
of modulo operations grows proportionally to the number of digits of the smaller
number.

```text
Average case: O(log n)
```

Therefore:

```text
Best case: O(1)
Average case: O(log n)
Worst case: O(log n)
```

## Summary Table

| Category | Algorithm | Best Case | Average Case | Worst Case |
| --- | --- | --- | --- | --- |
| Best case known, average/worst not fixed | Hill Climbing for N-Queens | Can be immediate, about `O(n^2)` for checking | Not generally fixed | May get stuck, cycle, or depend on step limit |
| Worst case known, average/best less meaningful | Simplex Algorithm | Can be very fast if already optimal | Hard to characterize generally | Exponential, often `O(2^n)` |
| All three cases can be analyzed | Euclidean Algorithm | `O(1)` | `O(log n)` | `O(log n)` |

## Final Conclusion

Hill climbing is a good example of an algorithm where the best case is easy to
identify, but average and worst cases depend too much on the implementation and
search behavior.

The Simplex Algorithm is a good example where the worst case is well known and
important theoretically, even though the algorithm is usually fast in practice.

The Euclidean Algorithm is the cleanest example because its best, average, and
worst cases can all be analyzed mathematically.
