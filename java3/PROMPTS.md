# Week 3: Prompts Used

These are the prompts used \for the Week 3 task, cleaned up
and translated from Albanian to English.

## Task: Organizational Hierarchy Analysis

File: `organizational_hierarchy.py`

The assignment (`Organizational_Hierarchy_Assignment.pdf`) gives 12 employees,
each with an `id`, `name`, `position`, `salary` and `supervisor_id`. The CEO
has `supervisor_id: null`, so the data forms one tree rooted at the CEO.
There are 5 problems, and every one must be solved with recursion.

### Prompt 1: Solve the assignment

```text
I am attaching Organizational_Hierarchy_Assignment.pdf. Read the whole PDF
before writing any code, then solve all 5 problems in Python.

Rules:
1. Follow the PDF exactly. Do not change any requirement, example output or
   return value.
2. Every problem must use recursion for the walk through the hierarchy.
   Loops are allowed only for bookkeeping: building an index, iterating over
   one employee's direct reports, and sorting the final result.
3. Build the indexes once, in O(n), before the recursion:
   - id -> employee, for walking up to the CEO (Problems 1, 3, 4)
   - supervisor_id -> direct reports, for walking down (Problems 2, 5)
   Never scan the whole employee list at each recursive step.
4. Keep the PDF's data shapes: the Employee, EmployeeData, Subordinate and
   CommonManager interfaces become Python TypedDicts with the same keys.
   Function names use Python style (get_employee_depth instead of
   getEmployeeDepth); null becomes None.
5. Handle every invalid input the PDF lists: a missing employee, a
   supervisor ID that does not exist, and a cycle in the supervisor chain.
   Detect cycles with a set of visited IDs passed down the recursion.
6. Problem 4 must reuse the recursive get_path_to_ceo from Problem 3,
   compute each path only once, check membership with a set, and return
   None before computing any path if either employee does not exist.

Deliverable: one runnable file, organizational_hierarchy.py, using only the
standard library, containing:
- the types and the dataset from the PDF
- the two index helpers and all 5 functions, each with a docstring and
  comments marking the base case and the recursive case
- tests that print PASS/FAIL for every example in the PDF, plus extra
  robustness tests (cycle, broken supervisor link, disconnected trees, empty
  list), clearly labelled as additional
```

### Prompt 2: Check against the PDF

```text
Go through the PDF again, requirement by requirement, and check the solution
against each one. For every requirement, say whether it is met and point to
the line of code that meets it. Fix anything that is missing, then run the
file and show the test output.
```

## Approach

Two indexes are built once per call, in `O(n)`:

- `build_employee_map`: `id -> employee`, used to go **up** the tree
  (Problems 1, 3, 4). Each step to a supervisor is `O(1)`.
- `build_children_map`: `supervisor_id -> direct reports`, used to go
  **down** the tree (Problems 2, 5). Each employee is visited once.

Without these indexes, every recursive step would have to scan the whole
list, which makes walking up `O(n * h)` instead of `O(n + h)`.

Every recursive walk also carries a `visited` set, so a broken or cyclic
supervisor chain can never make the recursion run forever.

## Problem 1: Employee Depth

```text
depth(CEO) = 0
depth(e)   = 1 + depth(supervisor of e)
```

- Base cases: the CEO returns `0`; a missing ID or an ID already in
  `visited` (a cycle) returns `-1`.
- Recursive case: ask for the supervisor's depth and add 1. A `-1` from the
  supervisor is passed straight back up.

```text
depth(12) = 1 + depth(7) = 1 + 1 + depth(4) = ... = 1 + 1 + 1 + 1 + 0 = 4
```

Time: `O(n)` for the index + `O(h)` for the walk. Space: `O(h)` call stack.

## Problem 2: All Subordinates

- Recursive case: record every direct report at `relative_depth`, then
  recurse into each of them with `relative_depth + 1`.
- Base case: an employee with no direct reports (the loop runs zero times).
- The result is sorted by `relative_depth`, then `id`, because the
  recursion goes deep before wide (it reaches Liam at depth 3 before Eve at
  depth 1).

Time: `O(n)` index + `O(k)` walk + `O(k log k)` sort, where `k` is the number
of subordinates. Space: `O(h)` call stack.

## Problem 3: Path to CEO

```text
path(CEO) = [CEO.id]
path(e)   = [e.id, *path(supervisor of e)]
```

```text
path(5) = [5, *path(2)] = [5, *[2, *path(1)]] = [5, 2, 1]
```

A real path always contains the CEO, so an empty list means failure (missing
ID, broken link or cycle).

Time: `O(n)` index + `h` calls; copying the list at each level adds up to
`O(h^2)`. Space: `O(h)` call stack.

## Problem 4: Lowest Common Manager

1. Return `None` if either ID is missing, before computing any path.
2. Reuse `get_path_to_ceo` once for each employee.
3. Put the second path in a `set` for `O(1)` membership checks.
4. Walk the first path recursively and stop at the first ID that is also in
   the set.

The first path goes from the employee upward, deepest first. Every manager
above the lowest common manager is shared, and nothing below it is, so the
first shared ID is the lowest one.

```text
(12, 9): path1 = [12, 7, 4, 2, 1], set = {9, 5, 2, 1}
         12, 7, 4 are not shared; 2 is, at position 3
         2 is at position 2 in [9, 5, 2, 1]
         -> Bob Smith, distances 3 and 2
```

An employee counts as their own ancestor because each path starts with the
employee, so `(7, 7)` gives `7, 0, 0` and `(1, 12)` gives `1, 0, 4`. Two
disconnected trees share no ID, so the result is `None`.

Time: `O(n + h^2)`. Space: `O(h)`.

## Problem 5: Team Salary

```text
teamSalary(e) = e.salary + sum(teamSalary(c)) for every direct report c
```

- Base case: a leaf employee has no direct reports, so the result is their
  own salary (`teamSalary(12) = 50000`).
- Recursive case: `teamSalary(7) = 120000 + teamSalary(12) = 170000`.

Time: `O(n)` index + `O(k)` walk. Space: `O(h)` call stack.

## Final results

Run with `python organizational_hierarchy.py`.

| Problem | Example | Result |
|---|---|---|
| 1 | depth of 1, 2, 7, 12, 999 | 0, 1, 3, 4, -1 |
| 2 | subordinates of 2 | 4, 5 (depth 1); 7, 8, 9, 10 (depth 2); 12 (depth 3) |
| 2 | subordinates of 6, 12, 999 | [11], [], [] |
| 3 | path of 12, 1, 5, 999 | [12, 7, 4, 2, 1], [1], [5, 2, 1], [] |
| 4 | (12, 9), (8, 10), (1, 12), (7, 7) | Bob 3/2, David 1/1, Alice 0/4, Grace 0/0 |
| 4 | (999, 1) | None |
| 5 | team salary of 1, 4, 7, 12, 999 | 1490000, 505000, 170000, 50000, 0 |

All 43 tests pass: 23 from the PDF examples and 20 additional robustness
tests (cycles, broken links, disconnected trees, empty list).
