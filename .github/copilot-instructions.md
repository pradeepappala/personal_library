# Copilot Instructions for personal_library

## Project Overview
This is a Kivy-based desktop/mobile app for managing a personal book library, with SQLite as the backend.
Main UI logic is in `main.py`, using Kivy screens for each operation. Book-related operations (add/show/remove/borrow/return books, get borrowed books with lender details) are grouped under the "Manage Books" screen. Lender-related operations (add/show/remove lenders) are grouped under the "Manage Lendors" screen. Other screens handle details and data management.
Core backend logic is in `src/personal_library.py` (class `PersonalLibrary`), which handles all database operations and queries.

## Architecture & Data Flow
UI screens interact with a single `PersonalLibrary` instance (`library`) for all operations.
Data flows from UI (user input) → backend (`PersonalLibrary` methods) → SQLite DB → UI (results displayed).
Each screen is a Kivy `Screen` subclass, with a scrollable result label for displaying output (see `ScrollView` usage in `main.py`).
All book/lender/borrowed records are stored in SQLite tables: `books`, `lendors`, `borrowed`.

## Developer Workflows
**Setup:**
  - Create and activate a Python venv (`library_venv`).
  - Install dependencies: `pip install -r requirements.txt`.
**Run UI:**
  - Start with `python -m main` (from repo root).
  - In VS Code, select the venv Python interpreter and run (`F5`/`Ctrl+F5`).
**Testing:**
  - Unit tests are in `tests/unittests/test_personal_library.py`.
  - Run tests with `python -m unittest discover tests/unittests`.
**Build Android APK:**
  - Use Buildozer (see README for setup and commands).

## Project-Specific Patterns & Conventions
All Kivy screens use a vertical `BoxLayout` and a scrollable result label for output.
Book-related screens are grouped under `ManageBooksScreen`, and lender-related screens under `ManageLendorsScreen` for better organization and navigation.
Database schema is created automatically if missing (see `create_tables` in `PersonalLibrary`).
Book/lender IDs are auto-incremented integers; borrowed status is tracked via the `returned` field in `borrowed` table.
UI navigation is managed via Kivy's `ScreenManager`.
All backend methods return raw DB rows; formatting for display is handled in the UI layer.
No ORM is used; direct SQL queries via `sqlite3`.

## Data Import/Export (xls)
- All data import/export is now handled via xls file for maximum compatibility, especially on Android.
- Export: `library.export_to_excel(folder_path)` saves:
  - `/sdcard/Download/mylibrary/<name>.xls` for Android
  - `os.path.join(os.path.expanduser('~'), 'work/personal_library', '<name>.xls')` for Windows/Linux/macOS
- Import: `library.import_from_excel(folder_path)` loads data from these xls files and overwrites the tables.
- No Excel or pandas ExcelWriter is used for import/export; only pandas xls methods are required.

## Integration Points
Kivy for UI (`main.py`)
SQLite for persistence (`src/personal_library.py`)
Buildozer for Android packaging (see README)

## Key Files & Directories
- `main.py`: Kivy UI, screen logic, app entry point. Includes `ManageBooksScreen` and `ManageLendorsScreen` for grouped book/lender operations.
- `src/personal_library.py`: Backend, DB logic
- `requirements.txt`: Python dependencies
- `README.md`: Setup, build, and run instructions
- `tests/unittests/test_personal_library.py`: Unit tests

## Example Patterns
- To add a book: `library.add_book(title, author)`
- To show all books: `library.get_all_books()` → format results for display
- To borrow a book: `library.borrow_book(lendor_id, book_id)`
- To return a book: `library.return_borrowed_book(borrowed_id)`
- To export all tables: `library.export_to_excel(folder_path)`
  - Windows/Linux/macOS: `os.path.join(os.path.expanduser('~'), 'work/personal_library')`
  - Android: `r'/sdcard/Download/mylibrary'`
- To import all tables: `library.import_from_excel(folder_path)`
  - Windows/Linux/macOS: `os.path.join(os.path.expanduser('~'), 'work/personal_library')`
  - Android: `r'/sdcard/Download/mylibrary'`

---

If any section is unclear or missing important details, please provide feedback to improve these instructions.
