# Debugging Report

## Setup Summary

1.  **Virtual Environment**: A virtual environment was created and activated to isolate project dependencies:
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    ```
2.  **Dependencies**: Project dependencies were installed from `requirements.txt` using pip.
    ```bash
    pip install -r requirements.txt
    ```
3.  **VS Code Debugger**: A `launch.json` file was created inside a `.vscode` directory to configure the VS Code debugger for running the Django development server and tests. This allows for setting breakpoints and inspecting variables directly within the editor.

## Bug Analysis

### Bug 1: AttributeError

*   **Cause**: The code `request.GET.get('q').strip()` caused an `AttributeError`. When the `q` query parameter is not present in the URL, `request.GET.get('q')` returns `None`. Calling `.strip()` on `None` raises the exception because the `NoneType` object does not have a `strip` method.
*   **Discovery**: I set a breakpoint on the line `query = request.GET.get('q').strip()`. After starting the debugger (`F5`) and navigating to `http://127.0.0.1:8000/buggy/` (without any query parameters), the debugger paused. Stepping over (`F10`) immediately triggered an "Uncaught Exception" for `AttributeError`.
*   **Fix**: I changed the line to `query = (request.GET.get('q') or "").strip()`. This ensures that if `request.GET.get('q')` is `None`, it is replaced with an empty string `""` before `.strip()` is called, preventing the error.

### Bug 2: Logic Error (`is` vs `==`)

*   **Cause**: The code `if field_filter is not 'All':` used the `is not` operator to compare strings. In Python, `is` checks for object identity (whether two variables point to the exact same object in memory), whereas `==` checks for equality (whether two objects have the same value). While this might work sometimes due to string interning, it is not reliable for string comparison.
*   **Discovery**: I set a breakpoint on the `if` statement. I navigated to `http://127.0.0.1:8000/buggy/?q=ai&field=All`. When the breakpoint was hit, I used the "Variables" panel in VS Code to inspect `field_filter` and confirmed its value was the string `"All"`. However, stepping over the line showed that the `if` block was still entered, which was incorrect behavior. This indicated an issue with the comparison logic.
*   **Fix**: I replaced `is not` with `!=` to correctly compare the string values: `if field_filter != 'All':`. This ensures the comparison is based on the content of the string, not its memory address.

### Bug 3: KeyError

*   **Cause**: The `predicate` function contained a typo in a dictionary key: `p['descriptionn']`. The correct key in the `ALL_PROJECTS` dataset is `description`. This caused a `KeyError` when the function tried to access a non-existent key.
*   **Discovery**: I set a breakpoint inside the `predicate` function. By navigating to `http://127.0.0.1:8000/buggy/?q=city`, I hit the breakpoint. The "Run and Debug" panel in VS Code has an option to "Break on Raised Exceptions," which I enabled. When stepping over the `return` statement, the debugger immediately halted and highlighted the `p['descriptionn']` part of the line, showing a `KeyError` in the exception pop-up.
*   **Fix**: I corrected the typo in the key from `descriptionn` to `description`, changing the line to `return query.lower() in p['title'].lower() or query.lower() in p['description'].lower()`.
