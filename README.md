# Team Project Work Allocation

## Team Members
1. **Alexander**
2. **Tyreke**
3. **Reagan**

---

## Work Allocation

### Alexander
- **Initial Commit**:
  - Implemented the basic structure of the project, including:
    - `login_prompt()` to establish the database connection.
    - `list_options()` to handle menu options.
    - A placeholder framework for CRUD operations (`display_all()`, etc.).
  - Ensured successful connection handling with basic menu navigation.

### Tyreke
- **Second Commit**:
  - Refactored the project to improve structure and functionality.
  - Implemented robust input validation in `list_options()` and numeric validation in `get_float_input()`.
  - Added `insert_display()` to handle adding new digital displays and their associated models.
  - Integrated parameterized SQL queries for security and reliability.
  - Committed changes for new model insertions in `insert_display()`.

### Reagan
- **Final Commit**:
  - Expanded the project functionality:
    - Added `scheduler_search()` to enable searching digital displays by scheduler system.
    - Improved `list_options()` to loop through menu navigation and handle invalid inputs gracefully.
    - Enhanced `insert_display()` with validation for serial numbers and model numbers.
  - Polished user interaction and added detailed success/error messages.
  - Implemented graceful logout with `logout()`.

---

## Team Representative
**Tyreke**  
Tyreke is the designated team representative responsible for submitting the project.

---

## Notes
- The project was divided into three key stages, reflecting contributions from Alexander, Tyreke, and Reagan.
- The final version integrates login, menu navigation, and CRUD operations with robust input validation and error handling.
