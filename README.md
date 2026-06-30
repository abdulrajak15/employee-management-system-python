#  Employee Management System — Console App
**Cognetix Technology Internship | Level 2 — Project 1**

---

## Objective
A database-driven Python console application to manage employee records with full CRUD operations using SQLite.

---

## Features
| Feature | Description |
|---|---|
| Add Employee | Collects & validates ID, Name, Email, Department, Salary |
| View All Employees | Displays all records in a formatted table |
| Search Employee | Find any employee instantly by ID |
| Update Employee | Edit any field; press ENTER to keep existing value |
| Delete Employee | Remove record with confirmation prompt |
| SQLite Database | Auto-creates `employees.db` — no installation needed |

---

## Database Schema

**Table: `employees`**

| Field | Type | Constraint |
|---|---|---|
| emp_id | INTEGER | PRIMARY KEY, UNIQUE |
| name | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| department | TEXT | NOT NULL |
| salary | REAL | NOT NULL |

---

## Folder Structure
```
employee_management/
├── app.py          ← Main application (menu + CRUD logic)
├── database.py     ← DB utility (connection, queries)
├── employees.db    ← Auto-created SQLite database
└── README.md       ← This file
```

---

## How to Run

### 1. Verify Python is installed
```bash
python --version   # must be 3.x
```

### 2. Navigate to the project folder
```bash
cd employee_management
```

### 3. Run the application
```bash
python app.py
```
> No pip install needed — only built-in `sqlite3` module is used.

---

## Sample Input / Output

### Add Employee
```
── ADD EMPLOYEE ─────────────────────────
  Employee ID   : 101
  Full Name     : Rahul Sharma
  Email         : rahul@cognetix.com
  Department    : Engineering
  Salary (₹)    : 75000
  [SUCCESS] Employee 'Rahul Sharma' (ID: 101) added successfully.
```

### View All Employees
```
── ALL EMPLOYEES ────────────────────────

  ID     Name                 Email                        Department      Salary
  ──────────────────────────────────────────────────────────────────────────────────
  101    Rahul Sharma         rahul@cognetix.com           Engineering    ₹75,000.00
  102    Priya Patel          priya@cognetix.com           HR             ₹60,000.00

  Total records: 2
```

### Update Employee
```
── UPDATE EMPLOYEE ──────────────────────
  Enter Employee ID to update: 101

  Updating: Rahul Sharma | Engineering | ₹75,000.00
  (Press ENTER to keep current value)

  New Salary [₹75,000.00]: 85000
  [SUCCESS] Employee ID '101' updated successfully.
```

### Error Cases
```
  [ERROR] Employee ID '101' already exists.
  [ERROR] Email 'rahul@cognetix.com' is already registered.
  [ERROR] Salary must be a valid positive number.
  [NOT FOUND] No employee with ID '999'.
```

---

## Error Handling Covered
- Duplicate Employee ID
- Duplicate email address
- Non-numeric salary or ID
- Empty name / department fields
- Invalid email format
- Database connection / SQL errors

---

## Technologies Used
- **Language**: Python 3.x
- **Database**: SQLite via `sqlite3` (built-in)
- **Modules**: `sqlite3` only — no external libraries

---

## GitHub Submission Checklist
- [x] `app.py` — main application
- [x] `database.py` — DB utility module
- [x] `employees.db` — auto-created on first run
- [x] `README.md` — documentation
- [ ] Screenshots of all operations *(take after running locally)*
