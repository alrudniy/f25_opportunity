# Debugging Report — Dylan Brooks

## Setup Summary
- Created a new branch: Debug_DylanBrooks
- Activated virtual environment (.venv)
- Installed dependencies with: pip install -r requirements.txt
- Added Python interpreter in VS Code (Python: Select Interpreter → .venv)
- Created .vscode/launch.json with two configs:
  - Django: runserver
  - Django: manage.py test (debug)

## Bug 1 — AttributeError (NoneType .strip())
**Cause:** request.GET.get('q') returns None when the parameter is missing. None.strip() raises AttributeError.

**How I found it:**  
Breakpoint on the line, opened /buggy/, stepped over and saw exception in Debug Console.

**Fix:**  
Replaced: query = request.GET.get('q').strip()
With: query = (request.GET.get('q') or "").strip()

---

## Bug 2 — Logic error: "is" vs "=="
**Cause:** Using identity (`is not 'All'`) instead of equality caused the condition to behave incorrectly.

**How I found it:**  
Breakpoint on the if-statement, inspected variable values in VS Code.

**Fix:**  
Changed `is not` to `!=`.

---

## Bug 3 — KeyError: misspelled dictionary key
**Cause:** Used `'descriptionn'` instead of `'description'`.

**How I found it:**  
Breakpoint inside predicate, ran /buggy/?q=city, stepped in (F11) and saw KeyError.

**Fix:**  
Replaced `'descriptionn'` with `'description'`.
