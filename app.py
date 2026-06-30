"""
Employee Management System — Console App
Cognetix Technology Internship | Level 2 — Project 1
Language : Python 3.x
Database : SQLite (employees.db)
"""

from database import create_table, execute_query, fetch_all, fetch_one


# ─────────────────────────────────────────────
#  INPUT VALIDATION HELPERS
# ─────────────────────────────────────────────
def is_valid_email(email: str) -> bool:
    return "@" in email.strip()


def is_valid_salary(salary_str: str) -> bool:
    try:
        val = float(salary_str)
        return val >= 0
    except ValueError:
        return False


# ─────────────────────────────────────────────
#  DISPLAY HELPER
# ─────────────────────────────────────────────
def print_employee_table(rows) -> None:
    """Print employee records in a clean formatted table."""
    if not rows:
        print("  No employee records found.")
        return

    print(f"\n  {'ID':<6} {'Name':<20} {'Email':<28} {'Department':<15} {'Salary':>10}")
    print("  " + "─" * 82)
    for r in rows:
        print(
            f"  {r['emp_id']:<6} {r['name']:<20} {r['email']:<28} "
            f"{r['department']:<15} ₹{r['salary']:>9,.2f}"
        )
    print(f"\n  Total records: {len(rows)}")


# ─────────────────────────────────────────────
#  CRUD FUNCTIONS
# ─────────────────────────────────────────────
def add_employee() -> None:
    print("\n── ADD EMPLOYEE ─────────────────────────")

    # Employee ID
    try:
        emp_id = int(input("  Employee ID   : "))
    except ValueError:
        print("  [ERROR] ID must be a number.")
        return

    # Check duplicate ID
    if fetch_one("SELECT emp_id FROM employees WHERE emp_id = ?", (emp_id,)):
        print(f"  [ERROR] Employee ID '{emp_id}' already exists.")
        return

    # Name
    name = input("  Full Name     : ").strip()
    if not name:
        print("  [ERROR] Name cannot be empty.")
        return

    # Email
    email = input("  Email         : ").strip()
    if not is_valid_email(email):
        print("  [ERROR] Invalid email. Must contain '@'.")
        return

    # Check duplicate email
    if fetch_one("SELECT emp_id FROM employees WHERE email = ?", (email,)):
        print(f"  [ERROR] Email '{email}' is already registered.")
        return

    # Department
    department = input("  Department    : ").strip()
    if not department:
        print("  [ERROR] Department cannot be empty.")
        return

    # Salary
    salary_input = input("  Salary (₹)    : ").strip()
    if not is_valid_salary(salary_input):
        print("  [ERROR] Salary must be a valid positive number.")
        return
    salary = float(salary_input)

    # Insert into DB
    sql = "INSERT INTO employees (emp_id, name, email, department, salary) VALUES (?, ?, ?, ?, ?)"
    if execute_query(sql, (emp_id, name, email, department, salary)):
        print(f"  [SUCCESS] Employee '{name}' (ID: {emp_id}) added successfully.")
    else:
        print("  [FAILED] Could not add employee. Check for duplicate ID or email.")


def view_employees() -> None:
    print("\n── ALL EMPLOYEES ────────────────────────")
    rows = fetch_all("SELECT * FROM employees ORDER BY emp_id")
    print_employee_table(rows)


def search_employee() -> None:
    print("\n── SEARCH EMPLOYEE ──────────────────────")
    try:
        emp_id = int(input("  Enter Employee ID: "))
    except ValueError:
        print("  [ERROR] ID must be a number.")
        return

    row = fetch_one("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    if row:
        print(f"\n  ✔ Employee Found:")
        print(f"    ID         : {row['emp_id']}")
        print(f"    Name       : {row['name']}")
        print(f"    Email      : {row['email']}")
        print(f"    Department : {row['department']}")
        print(f"    Salary     : ₹{row['salary']:,.2f}")
    else:
        print(f"  [NOT FOUND] No employee with ID '{emp_id}'.")


def update_employee() -> None:
    print("\n── UPDATE EMPLOYEE ──────────────────────")
    try:
        emp_id = int(input("  Enter Employee ID to update: "))
    except ValueError:
        print("  [ERROR] ID must be a number.")
        return

    row = fetch_one("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    if not row:
        print(f"  [NOT FOUND] No employee with ID '{emp_id}'.")
        return

    print(f"\n  Updating: {row['name']} | {row['department']} | ₹{row['salary']:,.2f}")
    print("  (Press ENTER to keep current value)\n")

    # Name
    new_name = input(f"  New Name       [{row['name']}]: ").strip()
    if not new_name:
        new_name = row['name']

    # Email
    new_email = input(f"  New Email      [{row['email']}]: ").strip()
    if not new_email:
        new_email = row['email']
    elif not is_valid_email(new_email):
        print("  [ERROR] Invalid email format.")
        return

    # Department
    new_dept = input(f"  New Department [{row['department']}]: ").strip()
    if not new_dept:
        new_dept = row['department']

    # Salary
    new_salary_str = input(f"  New Salary     [₹{row['salary']:,.2f}]: ").strip()
    if not new_salary_str:
        new_salary = row['salary']
    elif not is_valid_salary(new_salary_str):
        print("  [ERROR] Salary must be a valid number.")
        return
    else:
        new_salary = float(new_salary_str)

    sql = """
        UPDATE employees
        SET name = ?, email = ?, department = ?, salary = ?
        WHERE emp_id = ?
    """
    if execute_query(sql, (new_name, new_email, new_dept, new_salary, emp_id)):
        print(f"  [SUCCESS] Employee ID '{emp_id}' updated successfully.")
    else:
        print("  [FAILED] Update failed. Email may already be in use.")


def delete_employee() -> None:
    print("\n── DELETE EMPLOYEE ──────────────────────")
    try:
        emp_id = int(input("  Enter Employee ID to delete: "))
    except ValueError:
        print("  [ERROR] ID must be a number.")
        return

    row = fetch_one("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    if not row:
        print(f"  [NOT FOUND] No employee with ID '{emp_id}'.")
        return

    confirm = input(
        f"  Confirm delete '{row['name']}' (ID: {emp_id})? [y/n]: "
    ).strip().lower()

    if confirm == "y":
        if execute_query("DELETE FROM employees WHERE emp_id = ?", (emp_id,)):
            print(f"  [SUCCESS] Employee ID '{emp_id}' deleted successfully.")
    else:
        print("  [CANCELLED] Deletion cancelled.")


# ─────────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────────
def display_menu() -> None:
    print("\n" + "=" * 44)
    print("    COGNETIX EMPLOYEE MANAGEMENT SYSTEM")
    print("=" * 44)
    print("  1. Add Employee")
    print("  2. View All Employees")
    print("  3. Search Employee")
    print("  4. Update Employee")
    print("  5. Delete Employee")
    print("  6. Exit")
    print("=" * 44)


def main() -> None:
    print("\nWelcome to Cognetix Employee Management System!")
    create_table()
    print("  Database connected. Table ready.")

    while True:
        display_menu()
        choice = input("  Enter your choice (1-6): ").strip()

        if   choice == "1": add_employee()
        elif choice == "2": view_employees()
        elif choice == "3": search_employee()
        elif choice == "4": update_employee()
        elif choice == "5": delete_employee()
        elif choice == "6":
            print("\nGoodbye! Exiting Employee Management System.\n")
            break
        else:
            print("  [ERROR] Invalid choice. Enter a number between 1 and 6.")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
