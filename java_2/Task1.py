calls = 0
m2_calls = 0
mm_calls = 0


def m1(a):
    global calls
    calls += 1

    if len(a) <= 1:
        return len(a)
    mid = len(a) >> 1
    return m1(a[:mid]) + m1(a[mid:]) + 1


def m2(n):
    global m2_calls
    m2_calls += 1

    if n == 0:
        return 1
    return n - mm(m2(n - 1))


def mm(n):
    global mm_calls
    mm_calls += 1

    if n == 0:
        return 0
    return n - m2(mm(n - 1))


def m3(n):
    global calls
    calls += 1

    if n <= 1:
        return 1
    return m3(n - 1) + m3(n - 1)


def m3_fixed(n):
    global calls
    calls += 1

    if n <= 1:
        return 1
    return 2 * m3_fixed(n - 1)


def count(function, argument):
    """Run function(argument) and return (result, number_of_calls)."""
    global calls
    calls = 0
    result = function(argument)
    return result, calls


def count_m2(n):
    global m2_calls, mm_calls
    m2_calls = 0
    mm_calls = 0
    result = m2(n)
    return result, m2_calls, mm_calls


def check(prediction, actual):
    return "OK" if prediction == actual else "WRONG"


def show_m1():
    print("=" * 60)
    print("m1  -  called with an array of length 8")
    print("=" * 60)
    result, made = count(m1, list(range(8)))
    print(f"Returns: {result:<10} predicted 15        {check(15, result)}")
    print(f"Calls:   {made:<10} predicted 15        {check(15, made)}")
    print("Recurrence: T(n) = 2T(n/2) + 1, T(1) = 1  ->  2n - 1 calls, O(n)")
    print()
    print(f"  {'length':>6}{'returns':>10}{'calls':>8}{'2n - 1':>9}")
    for n in (1, 2, 4, 8, 16, 32):
        result, made = count(m1, list(range(n)))
        print(f"  {n:>6}{result:>10}{made:>8}{2 * n - 1:>9}")
    print()


def show_m2():
    print("=" * 60)
    print("m2(20)  -  m2 and mm call each other inside their argument")
    print("=" * 60)
    result, only_m2, only_mm = count_m2(20)
    print(f"Returns: {result:<10} not predictable by reading")
    print(f"Calls:   {only_m2 + only_mm:<10} not predictable by reading")
    print(f"  calls to m2 only : {only_m2}")
    print(f"  calls to mm only : {only_mm}")
    print(f"  m2 + mm together : {only_m2 + only_mm}")
    print("Recurrence: none in terms of n - the next argument is the")
    print("            result of another call (mm(m2(n - 1))).")
    print()
    print(f"  {'n':>6}{'returns':>10}{'m2 calls':>10}{'mm calls':>10}{'total':>8}")
    for n in range(21):
        result, only_m2, only_mm = count_m2(n)
        print(f"  {n:>6}{result:>10}{only_m2:>10}{only_mm:>10}{only_m2 + only_mm:>8}")
    print()


def show_m3():
    print("=" * 60)
    print("m3(20)")
    print("=" * 60)
    result, made = count(m3, 20)
    print(f"Returns: {result:<10} predicted 2^19 = 524288     {check(2 ** 19, result)}")
    print(f"Calls:   {made:<10} predicted 2^20 - 1 = 1048575 {check(2 ** 20 - 1, made)}")
    print("Recurrence: T(n) = 2T(n - 1) + 1, T(1) = 1  ->  2^n - 1 calls, O(2^n)")
    print("Wasted work: m3(n - 1) is computed twice with the same argument.")
    print()
    print(f"  {'n':>6}{'returns':>10}{'calls':>10}{'2^n - 1':>10}{'fixed calls':>13}")
    for n in range(1, 21):
        result, made = count(m3, n)
        _, fixed_made = count(m3_fixed, n)
        print(f"  {n:>6}{result:>10}{made:>10}{2 ** n - 1:>10}{fixed_made:>13}")
    print()


if __name__ == "__main__":
    show_m1()
    show_m2()
    show_m3()

    print("=" * 60)
    print("Summary (Task 1 table)")
    print("=" * 60)
    print(f"{'function':<16}{'returns':>10}{'calls':>12}")
    print("-" * 38)
    result, made = count(m1, list(range(8)))
    print(f"{'m1, length 8':<16}{result:>10}{made:>12}")
    result, only_m2, only_mm = count_m2(20)
    print(f"{'m2(20)':<16}{result:>10}{only_m2 + only_mm:>12}")
    result, made = count(m3, 20)
    print(f"{'m3(20)':<16}{result:>10}{made:>12}")
    print()
    print(f"m2(20): {only_m2} if only m2 calls are counted, "
          f"{only_m2 + only_mm} if m2 + mm are counted")
