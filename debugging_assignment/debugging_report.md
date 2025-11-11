# Debugging Report

## Setup Summary
- Created venv: `python -m venv .venv` and activated it.
- Installed deps: `pip install -r requirements.txt`.
- VS Code -> Python interpreter set to `.venv`.
- Added `.vscode/launch.json` with:
  - "Django: runserver"
  - "Django: manage.py test (debug)"

## Bugs & Fixes
### Bug 1 – AttributeError on missing `q`
- **Cause:** `request.GET.get('q').strip()` when `q` is missing (None.strip()).
- **Found with:** Breakpoint on the line, hit `/buggy/` (no params), saw traceback.
- **Fix:** `query = (request.GET.get('q') or '').strip()`.
- **Proof:** Screenshot of yellow highlight at the line + 500; then `/buggy_fixed/` returns 200 with Results.

### Bug 2 – `is` vs `==` (logic)
- **Cause:** `if field_filter is not 'All':` uses identity not equality.
- **Found with:** Breakpoint on that line; `/buggy/?q=ai&field=All` still filtered.
- **Fix:** `if field_filter != 'All':`
- **Proof:** `/buggy_fixed/?q=ai&field=All` shows unfiltered results; screenshot.

### Bug 3 – KeyError on misspelled dict key
- **Cause:** `'descriptionn'` instead of `'description'`.
- **Found with:** Breakpoint inside `predicate`; `/buggy/?q=city` 500 KeyError.
- **Fix:** `p['description']`.
- **Proof:** `/buggy_fixed/?q=city` returns 200 and lists the Smart City project.

## Screenshots
- Breakpoint/yellow-line captures for Bug 1 / Bug 2 / Bug 3.
- Browser 500 pages (buggy) vs 200 pages (fixed).
- Terminal server output showing requests and no tracebacks for `/buggy_fixed/`.
