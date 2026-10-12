# Week 3: Prompts Used

These are the prompts used for the Week 3 task, cleaned up
and translated from Albanian to English.

## Task: Organizational Hierarchy Analysis

File: `organizational_hierarchy.py`

The assignment (`Organizational_Hierarchy_Assignment.pdf`) gives 12 employees,
each with an `id`, `name`, `position`, `salary` and `supervisor_id`. The CEO
has `supervisor_id: null`, so the data forms one tree rooted at the CEO.
There are 5 problems, and every one must be solved with recursion.

### Prompt 1: Solve the assignment

````text
I have uploaded a PDF called Organizational_Hierarchy_Assignment.pdf.

Read the ENTIRE PDF carefully before solving anything. The PDF describes a
programming assignment about analyzing an organizational hierarchy
represented as a tree. Its signatures are written in TypeScript, but solve
it in PYTHON ONLY.

Your task is to solve ALL 5 problems in the PDF completely and correctly.

## VERY IMPORTANT RULES

1. Follow the PDF exactly. Do not replace its requirements with your own
   approach.
2. Every problem MUST use recursion for the actual hierarchy traversal.
3. Iterative loops are allowed ONLY for bookkeeping explicitly permitted by
   the PDF:
   - building a dict/index,
   - iterating over a node's children,
   - sorting the final result.
4. Do NOT scan the entire employees list at every recursive step when the
   PDF requires an index.
5. Translate the PDF's signatures to Python: snake_case function names, the
   same parameters, type hints, None instead of null, dict instead of Map,
   set instead of Set.
6. Turn the Employee, EmployeeData, Subordinate and CommonManager interfaces
   into TypedDicts with exactly the same keys.
7. Handle all invalid inputs required by the assignment.
8. Detect cycles wherever required.
9. Explain the recursive logic clearly enough that I can present it to my
   professor.
10. Do not skip any requirement, edge case or complexity requirement from
    the PDF.
11. Use only the Python standard library.

---

# DATASET

Use the exact employee dataset from the PDF (12 employees, from Alice
Johnson, CEO, id 1, to Liam Garcia, Intern Developer, id 12), with the
supervisor relationships and salaries exactly as provided.

---

# PROBLEM 1 - Calculate Employee Depth

```python
def get_employee_depth(employees: List[Employee], employee_id: int) -> int
```

Requirements:
- The CEO has depth 0, direct reports have depth 1, and so on upward:
  depth(e) = 1 + depth(supervisor).
- Return -1 if the employee does not exist, a supervisor does not exist, or
  the supervisor chain contains a cycle.
- Build an id -> employee dict ONCE, in O(n).
- The recursive walk must be O(h), where h is the hierarchy height.
- Use a set of visited IDs for cycle detection.

Required examples:
```python
get_employee_depth(employees, 1)    # 0
get_employee_depth(employees, 2)    # 1
get_employee_depth(employees, 7)    # 3
get_employee_depth(employees, 12)   # 4
get_employee_depth(employees, 999)  # -1
```

Explain the base case, the recursive case, cycle detection, and why the
complexity is O(n + h) rather than O(n * h).

---

# PROBLEM 2 - Get All Subordinates

```python
class Subordinate(TypedDict):
    id: int
    name: str
    relative_depth: int

def get_all_subordinates(employees: List[Employee], manager_id: int) -> List[Subordinate]
```

Requirements:
- Return ALL direct and indirect subordinates, NOT including the manager.
- Direct reports have relative_depth 1, their reports 2, and so on.
- Build a supervisor_id -> children index ONCE.
- Recursively traverse the subtree; visit each employee at most once.
- Return [] if the manager does not exist or has no subordinates.
- Sort by relative_depth ascending, then id ascending.

Required examples:
```python
get_all_subordinates(employees, 2)
# [{"id": 4, "name": "David Brown", "relative_depth": 1},
#  {"id": 5, "name": "Eve Davis", "relative_depth": 1},
#  {"id": 7, "name": "Grace Lee", "relative_depth": 2},
#  {"id": 8, "name": "Henry Martinez", "relative_depth": 2},
#  {"id": 9, "name": "Ivy Chen", "relative_depth": 2},
#  {"id": 10, "name": "Jack Thompson", "relative_depth": 2},
#  {"id": 12, "name": "Liam Garcia", "relative_depth": 3}]
get_all_subordinates(employees, 6)    # [{"id": 11, "name": "Kelly Anderson", "relative_depth": 1}]
get_all_subordinates(employees, 12)   # []
get_all_subordinates(employees, 999)  # []
```

Explain the recursive traversal and its complexity.

---

# PROBLEM 3 - Find Path to CEO

```python
def get_path_to_ceo(employees: List[Employee], employee_id: int) -> List[int]
```

Requirements:
- Return the employee IDs from the starting employee UP to the CEO,
  using recursion: path(e) = [e.id, *path(supervisor)].
- The CEO's path is [CEO_ID].
- Return [] if the employee doesn't exist, a supervisor doesn't exist, or
  the chain is cyclic. Detect cycles using a set.

Required examples:
```python
get_path_to_ceo(employees, 12)   # [12, 7, 4, 2, 1]
get_path_to_ceo(employees, 1)    # [1]
get_path_to_ceo(employees, 5)    # [5, 2, 1]
get_path_to_ceo(employees, 999)  # []
```

Explain the recursive relationship, the base case and cycle detection.

---

# PROBLEM 4 - Lowest Common Manager

```python
class CommonManager(TypedDict):
    manager_id: int
    manager_name: str
    distance_to_emp1: int
    distance_to_emp2: int

def find_lowest_common_manager(
    employees: List[Employee], emp_id1: int, emp_id2: int
) -> Optional[CommonManager]
```

IMPORTANT: the PDF requires reusing the recursive get_path_to_ceo from
Problem 3.

Requirements:
1. Validate both employees first; return None before computing any path if
   either does not exist.
2. Compute each path ONLY ONCE.
3. Use a set for membership checking instead of rescanning the second path.
4. Find the LOWEST common manager; the distances are its positions in each
   employee's path.
5. An employee counts as their own ancestor; handle emp_id1 == emp_id2.
6. Return None if the paths are broken, cyclic or in disconnected trees.

Required examples:
```python
find_lowest_common_manager(employees, 12, 9)
# {"manager_id": 2, "manager_name": "Bob Smith", "distance_to_emp1": 3, "distance_to_emp2": 2}
find_lowest_common_manager(employees, 8, 10)
# {"manager_id": 4, "manager_name": "David Brown", "distance_to_emp1": 1, "distance_to_emp2": 1}
find_lowest_common_manager(employees, 1, 12)
# {"manager_id": 1, "manager_name": "Alice Johnson", "distance_to_emp1": 0, "distance_to_emp2": 4}
find_lowest_common_manager(employees, 7, 7)
# {"manager_id": 7, "manager_name": "Grace Lee", "distance_to_emp1": 0, "distance_to_emp2": 0}
find_lowest_common_manager(employees, 999, 1)
# None
```

Explain carefully why the first common ID found in the first employee's path
is the LOWEST common manager.

---

# PROBLEM 5 - Total Team Salary

```python
def calculate_team_salary(employees: List[Employee], manager_id: int) -> int
```

Requirements:
- Use recursion: team_salary(e) = e.salary + sum(team_salary(c)) over every
  direct report c.
- Include the manager's own salary and every direct and indirect
  subordinate.
- Return 0 if the manager doesn't exist.

Required examples:
```python
calculate_team_salary(employees, 1)    # 1490000
calculate_team_salary(employees, 4)    # 505000
calculate_team_salary(employees, 7)    # 170000
calculate_team_salary(employees, 12)   # 50000
calculate_team_salary(employees, 999)  # 0
```

Explain the base case for a leaf employee and the recursive case for
managers.

---

# FINAL DELIVERABLE

1. Complete Python solution: ONE runnable file, organizational_hierarchy.py,
   with the TypedDicts, the dataset, the helper functions, all 5 functions
   and test cases that print PASS/FAIL. Run with:
   python organizational_hierarchy.py
   No placeholders; everything must be implemented.
2. Problem-by-problem explanation: what the problem asks, the data
   structure used, base case, recursive case, cycle detection, time and
   space complexity, with small examples from the dataset.
3. Complexity table (n = number of employees, h = hierarchy height,
   k = employees in a manager's subtree), separating the index-building
   cost from the recursive traversal cost.
4. Test output for all the PDF examples.
5. Edge cases: CEO, leaf employee, middle manager, non-existent employee,
   employee with no subordinates, employee as their own common manager,
   one employee being the ancestor of another, broken supervisor reference,
   cyclic supervisor reference, disconnected hierarchy, empty employee
   list. Label anything the PDF does not require as an additional
   robustness test.
6. Recursion concepts in beginner-friendly terms: the recursive call and
   base case in each problem, what the call stack stores, why the recursion
   depth depends on h, why building an index before recursing improves
   complexity, and the difference between time complexity and call-stack
   space.

Do NOT introduce advanced algorithms that are not needed. The answer must
be complete enough that I can submit the code and explain it orally to my
professor.
````

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
