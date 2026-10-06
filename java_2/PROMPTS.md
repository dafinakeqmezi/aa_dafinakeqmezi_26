# Week 2: Prompts Used

These are the prompts used with Claude Code for the Week 2 tasks, translated
from Albanian to English.

## Task: Recursion vs Iteration

File: `recursion_vs_iteration.py`

### Prompt 1

```text
A function where recursion and iteration have the same performance in Time
and Space.
A function where one version (e.g. the recursive one) degrades performance
in both time and space.
```

This section compares recursive and iterative versions of the same function in
terms of time and space complexity.

The selected functions are:

1. In-order traversal of a binary tree: recursion and iteration have the
   **same** time and space complexity.
2. Fibonacci numbers: the recursive version **degrades** both time and space.

### 1. Same Performance: In-order Traversal of a Binary Tree

In-order traversal visits the left subtree, then the node, then the right
subtree.

#### Recursive version

```text
visit(node):
    if node is empty: return
    visit(node.left)
    output node.value
    visit(node.right)
```

#### Iterative version

```text
stack = empty, node = root
while node is not empty or stack is not empty:
    while node is not empty:
        push node; node = node.left
    node = pop()
    output node.value
    node = node.right
```

#### Time

Both versions visit every node exactly once.

- Recursive: one call per node (plus calls on empty children), `O(n)`.
- Iterative: every node is pushed once and popped once, `O(n)`.

```text
Recursive time: O(n)
Iterative time: O(n)
```

#### Space

A tree traversal has to remember the path from the root to the current node,
so it can go back up after finishing a left subtree.

- The recursive version keeps that path in the **call stack**.
- The iterative version keeps the same path in an **explicit stack**.

In both cases, the stack holds at most `h` elements, where `h` is the height of
the tree.

```text
Recursive space: O(h)
Iterative space: O(h)

Balanced tree: h = O(log n)
Skewed tree:   h = O(n)
```

The iterative version does not save memory. It only moves the stack from the
call stack to a list. Recursion and iteration are equivalent here because the
problem needs a stack either way.

#### Measurements

| tree     | n         | recursive ms | iterative ms | recursive stack | iterative stack |
|----------|----------:|-------------:|-------------:|----------------:|----------------:|
| balanced | 1,000     | 0.23         | 0.12         | 10              | 9               |
| balanced | 10,000    | 1.81         | 1.15         | 14              | 13              |
| balanced | 100,000   | 20.66        | 16.50        | 17              | 16              |
| balanced | 1,000,000 | 207.59       | 170.41       | 20              | 19              |
| skewed   | 100       | 0.06         | 0.02         | 100             | 100             |
| skewed   | 500       | 0.20         | 0.08         | 500             | 500             |
| skewed   | 900       | 0.28         | 0.11         | 900             | 900             |

Both versions grow linearly in time, and the iterative one is only faster by a
constant factor because Python function calls are slower than list operations.
The stack size is the same: about `log2(n)` for a balanced tree and exactly
`n` for a skewed tree. The difference of 1 on balanced trees comes from where
each version records the stack size and is not important.

Note: the recursive version stops working on very deep trees, because Python
limits recursion depth to about 1000. This is a limit of the language, not of
the complexity.

### 2. Recursion Degrades Performance: Fibonacci Numbers

```text
fib(0) = 0
fib(1) = 1
fib(n) = fib(n - 1) + fib(n - 2)
```

#### Recursive version

```text
fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```

#### Iterative version

```text
a = 0, b = 1
repeat n times:
    a, b = b, a + b
return a
```

#### Time

The recursive version solves the same subproblems again and again. For example,
`fib(5)` calls `fib(3)` twice and `fib(2)` three times.

```text
                 fib(5)
              /         \
         fib(4)          fib(3)
        /     \          /    \
    fib(3)   fib(2)   fib(2) fib(1)
    /   \     /  \     /  \
 fib(2) fib(1) ...    ...
```

The number of calls is `T(n) = T(n - 1) + T(n - 2) + 1`, which grows like
Fibonacci itself, about `1.618^n`.

The iterative version computes every value from `0` to `n` once.

```text
Recursive time: O(phi^n), approximately O(1.618^n)  (exponential)
Iterative time: O(n)                                 (linear)
```

#### Space

- Recursive: the deepest chain of calls is `fib(n) -> fib(n-1) -> ... -> fib(1)`,
  so the call stack grows to `n` frames.
- Iterative: only two variables, `a` and `b`, no matter how big `n` is.

```text
Recursive space: O(n)
Iterative space: O(1)
```

#### Measurements

| n  | fib(n)  | recursive calls | iterative steps | recursive ms | iterative ms | recursive stack | iterative variables |
|---:|--------:|----------------:|----------------:|-------------:|-------------:|----------------:|--------------------:|
| 5  | 5       | 15              | 5               | 0.01         | 0.0039       | 5               | 2                   |
| 10 | 55      | 177             | 10              | 0.02         | 0.0010       | 10              | 2                   |
| 15 | 610     | 1,973           | 15              | 0.22         | 0.0011       | 15              | 2                   |
| 20 | 6,765   | 21,891          | 20              | 2.40         | 0.0011       | 20              | 2                   |
| 25 | 75,025  | 242,785         | 25              | 26.92        | 0.0012       | 25              | 2                   |
| 30 | 832,040 | 2,692,537       | 30              | 299.05       | 0.0092       | 30              | 2                   |

Every time `n` grows by 5, the recursive version needs about 11 times more calls
and time (`1.618^5 ≈ 11`). For `n = 30` it makes 2.7 million calls where the
iterative version needs 30 steps. The recursive stack also grows with `n`,
while the iterative version always uses the same two variables.

### Summary

| function             | version   | time            | space    |
|----------------------|-----------|-----------------|----------|
| In-order traversal   | recursive | O(n)            | O(h)     |
| In-order traversal   | iterative | O(n)            | O(h)     |
| Fibonacci            | recursive | O(1.618^n)      | O(n)     |
| Fibonacci            | iterative | O(n)            | O(1)     |

Recursion itself is not slow. It costs the same as iteration when the problem
needs a stack anyway, like tree traversal. It becomes a problem when the
recursive calls repeat the same work, like Fibonacci, or when they keep stack
frames that an iterative version does not need.

## Task 1: Trace (m1, m2, m3)

File: `Task1.py`

### Prompt 1

The task slides were attached as images, and the full slide text was pasted
in a later message.

```text
Continue with Task 1 and complete the remaining solutions:
the trace, then m1, m2, m3.
```

Task text from the slides:

```text
TASK 1 - Trace

Three functions follow, one per slide. For each one, write down what it
returns and how many calls it makes - before you type anything.

                 Returns   Calls
m1, length 8
m2(20)
m3(20)

Copy all three into your own file, add the counter from the sheet, and check.
One of the three cannot be predicted by reading it. Which one, and why?

m1 - called with an array of length 8:

function m1(a) {
  if (a.length <= 1) return a.length;
  const mid = a.length >> 1;
  return m1(a.slice(0, mid)) + m1(a.slice(mid)) + 1;
}

m2 - two functions that call each other, and each one calls the other
inside its own argument:

function m2(n) {
  if (n === 0) return 1;
  return n - mm(m2(n - 1));
}

function mm(n) {
  if (n === 0) return 0;
  return n - m2(mm(n - 1));
}

m3 - "Nothing here is wasted - or is it? Write the recurrence for this one
as well.":

function m3(n) {
  if (n <= 1) return 1;
  return m3(n - 1) + m3(n - 1);
}
```

### Prompt 2

```text
In Task1.py, change how the calls of m2 are counted so they are counted
separately:
- use two separate counters: one for calls to m2 and one for calls to mm
- reset both counters before every run of m2(n)

In the "m2(20)" section of the output, add these lines below "Returns" and
"Calls":
  calls to m2 only : 814
  calls to mm only : 813
  m2 + mm together : 1627

In the m2 table for n = 0..20, replace the "calls" column with three columns:
  n | returns | m2 calls | mm calls | total

In the "Summary (Task 1 table)" table, keep 1627 as the main value for
m2(20), but add a note below it:
  "m2(20): 814 if only m2 calls are counted, 1627 if m2 + mm are counted"

Do not change anything else in m1, m3 or m3_fixed. After the change, run
python Task1.py and verify that:
- m2 calls + mm calls = total for every n
- for n = 20: m2 = 814, mm = 813, total = 1627, returns = 13
```

### Final results

| function     | returns | calls                              |
|--------------|---------|------------------------------------|
| m1, length 8 | 15      | 15                                 |
| m2(20)       | 13      | 1627 (814 to m2 + 813 to mm)       |
| m3(20)       | 524288  | 1048575                            |

The function that cannot be predicted by reading it is **m2**: the argument
of each outer call is the result of another call (`mm(m2(n - 1))`), so there
is no recurrence in terms of `n` alone.
