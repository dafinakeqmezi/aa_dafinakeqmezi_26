import random


def count_conflicts(board):
    conflicts = 0
    n = len(board)

    for col1 in range(n):
        for col2 in range(col1 + 1, n):
            row1 = board[col1]
            row2 = board[col2]

            same_row = row1 == row2
            same_diagonal = abs(row1 - row2) == abs(col1 - col2)

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts


def hill_climbing_n_queens(n, max_steps=1000):
    board = [random.randint(0, n - 1) for _ in range(n)]

    for step in range(max_steps):
        current_conflicts = count_conflicts(board)

        if current_conflicts == 0:
            return board, step, True

        best_board = board[:]
        best_conflicts = current_conflicts

        for col in range(n):
            original_row = board[col]

            for row in range(n):
                if row == original_row:
                    continue

                candidate = board[:]
                candidate[col] = row
                candidate_conflicts = count_conflicts(candidate)

                if candidate_conflicts < best_conflicts:
                    best_conflicts = candidate_conflicts
                    best_board = candidate

        if best_conflicts >= current_conflicts:
            return board, step, False

        board = best_board

    return board, max_steps, False


def print_n_queens_board(board):
    for row in range(len(board)):
        line = ""
        for col in range(len(board)):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)


def simplex(c, a, b):
    number_of_constraints = len(a)
    number_of_variables = len(c)

    tableau = []

    for i in range(number_of_constraints):
        row = a[i][:]
        slack_variables = [0] * number_of_constraints
        slack_variables[i] = 1
        row += slack_variables
        row.append(b[i])
        tableau.append(row)

    objective_row = [-value for value in c]
    objective_row += [0] * number_of_constraints
    objective_row.append(0)
    tableau.append(objective_row)

    while min(tableau[-1][:-1]) < 0:
        pivot_column = tableau[-1][:-1].index(min(tableau[-1][:-1]))

        ratios = []
        for i in range(number_of_constraints):
            column_value = tableau[i][pivot_column]

            if column_value > 0:
                ratios.append(tableau[i][-1] / column_value)
            else:
                ratios.append(float("inf"))

        pivot_row = ratios.index(min(ratios))

        if ratios[pivot_row] == float("inf"):
            raise ValueError("The problem is unbounded.")

        pivot_value = tableau[pivot_row][pivot_column]

        tableau[pivot_row] = [
            value / pivot_value for value in tableau[pivot_row]
        ]

        for i in range(len(tableau)):
            if i == pivot_row:
                continue

            multiplier = tableau[i][pivot_column]
            tableau[i] = [
                tableau[i][j] - multiplier * tableau[pivot_row][j]
                for j in range(len(tableau[i]))
            ]

    solution = [0] * number_of_variables

    for variable_index in range(number_of_variables):
        column = [
            tableau[row][variable_index]
            for row in range(number_of_constraints)
        ]

        if column.count(1) == 1 and column.count(0) == number_of_constraints - 1:
            row_index = column.index(1)
            solution[variable_index] = tableau[row_index][-1]

    maximum_value = tableau[-1][-1]
    return solution, maximum_value


def gcd_euclidean(a, b):
    steps = 0

    while b != 0:
        a, b = b, a % b
        steps += 1

    return a, steps


def demo_hill_climbing():
    print("1. Hill Climbing for N-Queens")
    board, steps, solved = hill_climbing_n_queens(8)

    print("Solved:", solved)
    print("Steps:", steps)
    print("Conflicts:", count_conflicts(board))
    print_n_queens_board(board)
    print()


def demo_simplex():
    print("2. Simplex Algorithm")

    # Maximize: z = 3x + 5y
    # Subject to:
    #   x <= 4
    #   2y <= 12
    #   3x + 2y <= 18
    c = [3, 5]
    a = [
        [1, 0],
        [0, 2],
        [3, 2],
    ]
    b = [4, 12, 18]

    solution, maximum_value = simplex(c, a, b)

    print("x, y =", solution)
    print("Maximum value =", maximum_value)
    print()


def demo_gcd():
    print("3. Euclidean Algorithm for GCD")

    examples = [
        (20, 10),  # best case
        (34, 21),  # worst-case style: consecutive Fibonacci numbers
        (252, 105),  # normal example
    ]

    for a, b in examples:
        result, steps = gcd_euclidean(a, b)
        print(f"gcd({a}, {b}) = {result}, steps = {steps}")

    print()


if __name__ == "__main__":
    random.seed(7)
    demo_hill_climbing()
    demo_simplex()
    demo_gcd()
