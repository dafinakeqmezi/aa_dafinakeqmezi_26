import json
from typing import Dict, List, Optional, Set, TypedDict


class Employee(TypedDict):
    id: int
    name: str
    position: str
    salary: int
    supervisor_id: Optional[int]


class EmployeeData(TypedDict):
    employees: List[Employee]


class Subordinate(TypedDict):
    id: int
    name: str
    relative_depth: int


class CommonManager(TypedDict):
    manager_id: int
    manager_name: str
    distance_to_emp1: int
    distance_to_emp2: int


# ===========================================================================
# Dataset (exactly as given in the assignment)
# ===========================================================================

employee_data: EmployeeData = {
    "employees": [
        {"id": 1, "name": "Alice Johnson", "position": "CEO", "salary": 250000, "supervisor_id": None},
        {"id": 2, "name": "Bob Smith", "position": "CTO", "salary": 180000, "supervisor_id": 1},
        {"id": 3, "name": "Carol White", "position": "CFO", "salary": 175000, "supervisor_id": 1},
        {"id": 4, "name": "David Brown", "position": "Engineering Manager", "salary": 140000, "supervisor_id": 2},
        {"id": 5, "name": "Eve Davis", "position": "QA Manager", "salary": 130000, "supervisor_id": 2},
        {"id": 6, "name": "Frank Wilson", "position": "Senior Accountant", "salary": 95000, "supervisor_id": 3},
        {"id": 7, "name": "Grace Lee", "position": "Senior Developer", "salary": 120000, "supervisor_id": 4},
        {"id": 8, "name": "Henry Martinez", "position": "Junior Developer", "salary": 85000, "supervisor_id": 4},
        {"id": 9, "name": "Ivy Chen", "position": "QA Engineer", "salary": 90000, "supervisor_id": 5},
        {"id": 10, "name": "Jack Thompson", "position": "DevOps Engineer", "salary": 110000, "supervisor_id": 4},
        {"id": 11, "name": "Kelly Anderson", "position": "Junior Accountant", "salary": 65000, "supervisor_id": 6},
        {"id": 12, "name": "Liam Garcia", "position": "Intern Developer", "salary": 50000, "supervisor_id": 7},
    ]
}

employees: List[Employee] = employee_data["employees"]


# ===========================================================================
# Helpers: indexes built once per call, in O(n)
# ===========================================================================

def build_employee_map(employees: List[Employee]) -> Dict[int, Employee]:
    """id -> employee. Lets the recursion jump to a supervisor in O(1)."""
    by_id: Dict[int, Employee] = {}
    for employee in employees:
        by_id[employee["id"]] = employee
    return by_id


def build_children_map(employees: List[Employee]) -> Dict[int, List[Employee]]:
    """supervisor_id -> direct reports. Lets the recursion find a node's children in O(1)."""
    children_of: Dict[int, List[Employee]] = {}
    for employee in employees:
        if employee["supervisor_id"] is None:
            continue
        children_of.setdefault(employee["supervisor_id"], []).append(employee)
    return children_of


# ===========================================================================
# Problem 1: Calculate Employee Depth
# ===========================================================================

def get_employee_depth(employees: List[Employee], employee_id: int) -> int:
    by_id = build_employee_map(employees)  # O(n), built once
    return depth_recursive(by_id, employee_id, set())  # O(h)


def depth_recursive(by_id: Dict[int, Employee], employee_id: int, visited: Set[int]) -> int:
    employee = by_id.get(employee_id)
    if employee is None:
        return -1  
    if employee_id in visited:
        return -1  # base case: cycle detected
    if employee["supervisor_id"] is None:
        return 0  
    visited.add(employee_id)
    supervisor_depth = depth_recursive(by_id, employee["supervisor_id"], visited) 
    return -1 if supervisor_depth == -1 else 1 + supervisor_depth 


# ===========================================================================
# Problem 2: Get All Subordinates
# ===========================================================================

def get_all_subordinates(employees: List[Employee], manager_id: int) -> List[Subordinate]:
    by_id = build_employee_map(employees)
    if manager_id not in by_id:
        return []  
    children_of = build_children_map(employees)  
    result: List[Subordinate] = []
    visited = {manager_id}  
    collect_subordinates(children_of, manager_id, 1, visited, result)

    result.sort(key=lambda s: (s["relative_depth"], s["id"]))
    return result


def collect_subordinates(
    children_of: Dict[int, List[Employee]],
    manager_id: int,
    relative_depth: int,
    visited: Set[int],
    result: List[Subordinate],
) -> None:
    
    for report in children_of.get(manager_id, []):
        if report["id"] in visited:
            continue 
        visited.add(report["id"])
        result.append({"id": report["id"], "name": report["name"], "relative_depth": relative_depth})
        collect_subordinates(children_of, report["id"], relative_depth + 1, visited, result)  


# ===========================================================================
# Problem 3: Find Path to CEO
# ===========================================================================

def get_path_to_ceo(employees: List[Employee], employee_id: int) -> List[int]:
    by_id = build_employee_map(employees)  # O(n), built once
    return path_recursive(by_id, employee_id, set())


def path_recursive(by_id: Dict[int, Employee], employee_id: int, visited: Set[int]) -> List[int]:
    """path(CEO) = [CEO.id]
    path(e)   = [e.id, *path(supervisor of e)]

    A real path always contains at least the CEO, so an empty list can
    safely mean "failed" (missing ID, broken link, or cycle).
    """
    employee = by_id.get(employee_id)
    if employee is None:
        return []  
    if employee_id in visited:
        return [] 
    if employee["supervisor_id"] is None:
        return [employee["id"]]  

    visited.add(employee_id)
    supervisor_path = path_recursive(by_id, employee["supervisor_id"], visited)  
    if not supervisor_path:
        return [] 
    return [employee["id"], *supervisor_path]


# ===========================================================================
# Problem 4: Lowest Common Manager
# ===========================================================================

def find_lowest_common_manager(
    employees: List[Employee], emp_id1: int, emp_id2: int
) -> Optional[CommonManager]:
    """Find the lowest common manager of two employees.

    :param employees: List of employee objects
    :param emp_id1: First employee's ID
    :param emp_id2: Second employee's ID
    :returns: Object describing the common manager, or None if either employee
              does not exist or the two share no common manager
    """
    by_id = build_employee_map(employees)

    if emp_id1 not in by_id or emp_id2 not in by_id:
        return None

    path1 = get_path_to_ceo(employees, emp_id1)
    path2 = get_path_to_ceo(employees, emp_id2)
    if not path1 or not path2:
        return None  

    path2_ids = set(path2)
    distance1 = find_first_shared_index(path1, 0, path2_ids)
    if distance1 == -1:
        return None 

    manager = by_id[path1[distance1]]  
    return {
        "manager_id": manager["id"],
        "manager_name": manager["name"],
        "distance_to_emp1": distance1,  
        "distance_to_emp2": path2.index(manager["id"]),  
    }


def find_first_shared_index(path: List[int], index: int, other_path_ids: Set[int]) -> int:
    if index >= len(path):
        return -1
    if path[index] in other_path_ids:
        return index
    return find_first_shared_index(path, index + 1, other_path_ids)


# ===========================================================================
# Problem 5: Total Team Salary
# ===========================================================================

def calculate_team_salary(employees: List[Employee], manager_id: int) -> int:
    by_id = build_employee_map(employees)
    manager = by_id.get(manager_id)
    if manager is None:
        return 0  

    children_of = build_children_map(employees)  
    return team_salary_recursive(children_of, manager, set())


def team_salary_recursive(
    children_of: Dict[int, List[Employee]], employee: Employee, visited: Set[int]
) -> int:
    visited.add(employee["id"]) 
    total = employee["salary"]
    for report in children_of.get(employee["id"], []):
        if report["id"] not in visited:
            total += team_salary_recursive(children_of, report, visited)  # recursive case
    return total


# ===========================================================================
# Tests
# ===========================================================================

passed = 0
failed = 0


def check(label, actual, expected) -> None:
    global passed, failed
    ok = actual == expected
    if ok:
        passed += 1
    else:
        failed += 1
    detail = "" if ok else f"   (expected {json.dumps(expected)})"
    print(f"  [{'PASS' if ok else 'FAIL'}] {label} -> {json.dumps(actual)}{detail}")


def make_employee(emp_id: int, supervisor_id: Optional[int], salary: int = 1000) -> Employee:
    return {"id": emp_id, "name": f"Employee {emp_id}", "position": "Test",
            "salary": salary, "supervisor_id": supervisor_id}


cyclic_employees = [make_employee(1, None), make_employee(2, 3), make_employee(3, 2), make_employee(4, 3)]
broken_employees = [make_employee(1, None), make_employee(2, 99)]
disconnected_employees = [make_employee(1, None), make_employee(2, 1), make_employee(10, None), make_employee(11, 10)]
no_employees: List[Employee] = []


def run_tests() -> None:
    print("Problem 1: get_employee_depth")
    check("Employee 1 (CEO)", get_employee_depth(employees, 1), 0)
    check("Employee 2", get_employee_depth(employees, 2), 1)
    check("Employee 7", get_employee_depth(employees, 7), 3)
    check("Employee 12", get_employee_depth(employees, 12), 4)
    check("Employee 999 (not found)", get_employee_depth(employees, 999), -1)
    print("  Additional robustness tests:")
    check("Cyclic: employee 2 on a cycle", get_employee_depth(cyclic_employees, 2), -1)
    check("Cyclic: employee 4 leads into a cycle", get_employee_depth(cyclic_employees, 4), -1)
    check("Cyclic: CEO still works", get_employee_depth(cyclic_employees, 1), 0)
    check("Broken: supervisor 99 missing", get_employee_depth(broken_employees, 2), -1)
    check("Empty employee list", get_employee_depth(no_employees, 1), -1)

    print("\nProblem 2: get_all_subordinates")
    check("Manager 2", get_all_subordinates(employees, 2), [
        {"id": 4, "name": "David Brown", "relative_depth": 1},
        {"id": 5, "name": "Eve Davis", "relative_depth": 1},
        {"id": 7, "name": "Grace Lee", "relative_depth": 2},
        {"id": 8, "name": "Henry Martinez", "relative_depth": 2},
        {"id": 9, "name": "Ivy Chen", "relative_depth": 2},
        {"id": 10, "name": "Jack Thompson", "relative_depth": 2},
        {"id": 12, "name": "Liam Garcia", "relative_depth": 3},
    ])
    check("Manager 6", get_all_subordinates(employees, 6), [
        {"id": 11, "name": "Kelly Anderson", "relative_depth": 1},
    ])
    check("Manager 12 (no subordinates)", get_all_subordinates(employees, 12), [])
    check("Manager 999 (not found)", get_all_subordinates(employees, 999), [])
    print("  Additional robustness tests:")
    check("CEO: everyone except the CEO", len(get_all_subordinates(employees, 1)), 11)
    check("Cyclic: stops, each employee once", get_all_subordinates(cyclic_employees, 2), [
        {"id": 3, "name": "Employee 3", "relative_depth": 1},
        {"id": 4, "name": "Employee 4", "relative_depth": 2},
    ])
    check("Empty employee list", get_all_subordinates(no_employees, 1), [])

    print("\nProblem 3: get_path_to_ceo")
    check("Employee 12", get_path_to_ceo(employees, 12), [12, 7, 4, 2, 1])
    check("Employee 1 (CEO)", get_path_to_ceo(employees, 1), [1])
    check("Employee 5", get_path_to_ceo(employees, 5), [5, 2, 1])
    check("Employee 999 (not found)", get_path_to_ceo(employees, 999), [])
    print("  Additional robustness tests:")
    check("Cyclic: employee 4 leads into a cycle", get_path_to_ceo(cyclic_employees, 4), [])
    check("Broken: supervisor 99 missing", get_path_to_ceo(broken_employees, 2), [])
    check("Empty employee list", get_path_to_ceo(no_employees, 1), [])

    print("\nProblem 4: find_lowest_common_manager")
    check("Employees 12 and 9", find_lowest_common_manager(employees, 12, 9), {
        "manager_id": 2, "manager_name": "Bob Smith", "distance_to_emp1": 3, "distance_to_emp2": 2})
    check("Employees 8 and 10", find_lowest_common_manager(employees, 8, 10), {
        "manager_id": 4, "manager_name": "David Brown", "distance_to_emp1": 1, "distance_to_emp2": 1})
    check("Employees 1 and 12 (1 is an ancestor of 12)", find_lowest_common_manager(employees, 1, 12), {
        "manager_id": 1, "manager_name": "Alice Johnson", "distance_to_emp1": 0, "distance_to_emp2": 4})
    check("Employees 7 and 7 (same employee)", find_lowest_common_manager(employees, 7, 7), {
        "manager_id": 7, "manager_name": "Grace Lee", "distance_to_emp1": 0, "distance_to_emp2": 0})
    check("Employees 999 and 1 (not found)", find_lowest_common_manager(employees, 999, 1), None)
    print("  Additional robustness tests:")
    check("Employees 12 and 4 (ancestor given second)", find_lowest_common_manager(employees, 12, 4), {
        "manager_id": 4, "manager_name": "David Brown", "distance_to_emp1": 2, "distance_to_emp2": 0})
    check("Employees 12 and 11 (different branches)", find_lowest_common_manager(employees, 12, 11), {
        "manager_id": 1, "manager_name": "Alice Johnson", "distance_to_emp1": 4, "distance_to_emp2": 3})
    check("Employees 1 and 999 (second not found)", find_lowest_common_manager(employees, 1, 999), None)
    check("Disconnected trees", find_lowest_common_manager(disconnected_employees, 2, 11), None)
    check("Cyclic chain", find_lowest_common_manager(cyclic_employees, 1, 4), None)
    check("Broken chain", find_lowest_common_manager(broken_employees, 1, 2), None)
    check("Empty employee list", find_lowest_common_manager(no_employees, 1, 2), None)

    print("\nProblem 5: calculate_team_salary")
    check("Manager 1 (root / CEO)", calculate_team_salary(employees, 1), 1490000)
    check("Manager 4 (middle manager)", calculate_team_salary(employees, 4), 505000)
    check("Manager 7 (middle manager)", calculate_team_salary(employees, 7), 170000)
    check("Manager 12 (leaf employee)", calculate_team_salary(employees, 12), 50000)
    check("Manager 999 (non-existent ID)", calculate_team_salary(employees, 999), 0)
    print("  Additional robustness tests:")
    check("Cyclic: stops, each salary once", calculate_team_salary(cyclic_employees, 2), 3000)
    check("Empty employee list", calculate_team_salary(no_employees, 1), 0)

    print(f"\n{passed} passed, {failed} failed")
    if failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()
