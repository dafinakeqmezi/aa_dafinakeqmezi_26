import time

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_balanced_tree(low, high):
    if low > high:
        return None

    mid = (low + high) // 2
    return Node(mid, build_balanced_tree(low, mid - 1), build_balanced_tree(mid + 1, high))


def build_skewed_tree(n):
    root = None
    for value in range(n):
        root = Node(value, left=root)
    return root


def inorder_recursive(root):
    result = []
    max_depth = 0

    def visit(node, depth):
        nonlocal max_depth
        if node is None:
            return

        max_depth = max(max_depth, depth)
        visit(node.left, depth + 1)
        result.append(node.value)
        visit(node.right, depth + 1)

    visit(root, 1)
    return result, max_depth


def inorder_iterative(root):
    result = []
    stack = []
    max_stack = 0
    node = root

    while node is not None or stack:
        while node is not None:
            stack.append(node)
            max_stack = max(max_stack, len(stack))
            node = node.left

        node = stack.pop()
        result.append(node.value)
        node = node.right

    return result, max_stack

def fibonacci_recursive(n):
    calls = 0
    max_depth = 0

    def fib(k, depth):
        nonlocal calls, max_depth
        calls += 1
        max_depth = max(max_depth, depth)

        if k < 2:
            return k
        return fib(k - 1, depth + 1) + fib(k - 2, depth + 1)

    value = fib(n, 1)
    return value, calls, max_depth


def fibonacci_iterative(n):
    a, b = 0, 1
    steps = 0

    for _ in range(n):
        a, b = b, a + b
        steps += 1

    return a, steps, 2

def measure(function, *args):
    start = time.perf_counter()
    output = function(*args)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return output, elapsed_ms


def compare_tree_traversals():
    print("Case 1: In-order traversal (recursive vs iterative)")
    print("-" * 78)
    print(f"{'tree':<10}{'n':>9}{'rec ms':>11}{'iter ms':>11}{'rec stack':>12}{'iter stack':>12}{'same?':>8}")

    trees = [("balanced", n, build_balanced_tree(1, n)) for n in (1_000, 10_000, 100_000, 1_000_000)]
    trees += [("skewed", n, build_skewed_tree(n)) for n in (100, 500, 900)]

    for kind, n, root in trees:
        (rec_values, rec_stack), rec_ms = measure(inorder_recursive, root)
        (iter_values, iter_stack), iter_ms = measure(inorder_iterative, root)

        print(
            f"{kind:<10}{n:>9}{rec_ms:>11.2f}{iter_ms:>11.2f}"
            f"{rec_stack:>12}{iter_stack:>12}{str(rec_values == iter_values):>8}"
        )

    print()


def compare_fibonacci():
    print("Case 2: Fibonacci (recursive vs iterative)")
    print("-" * 78)
    print(f"{'n':>4}{'fib(n)':>10}{'rec calls':>12}{'iter steps':>12}{'rec ms':>11}{'iter ms':>10}{'rec stack':>11}{'iter vars':>10}")

    for n in (5, 10, 15, 20, 25, 30):
        (rec_value, calls, rec_stack), rec_ms = measure(fibonacci_recursive, n)
        (iter_value, steps, iter_vars), iter_ms = measure(fibonacci_iterative, n)
        assert rec_value == iter_value

        print(
            f"{n:>4}{rec_value:>10}{calls:>12}{steps:>12}"
            f"{rec_ms:>11.2f}{iter_ms:>10.4f}{rec_stack:>11}{iter_vars:>10}"
        )

    print()


if __name__ == "__main__":
    compare_tree_traversals()
    compare_fibonacci()
