# Copilot Instructions: Best Practices for Python Scripts (Windows 11, UV, PEP8)

## 1. Script Structure
- Each script should be self-contained and executable directly (include `if __name__ == "__main__":`).
- Place reusable logic in functions or classes.
- Add a docstring at the top describing the script's purpose, usage, and author.
- Use type hints for all function signatures.
- Handle exceptions gracefully and provide meaningful error messages.

## 2. File Naming & Organization
- Name scripts descriptively using lowercase and underscores (e.g., `data_cleaner.py`).
- **Use the following directory structure for organization:**
  - `dev/`: For scripts under active development or experimentation. Use this folder to iterate and test new features before moving scripts to production.
  - `scripts/`: For production-ready, self-executing scripts. Only the latest, stable versions should be stored here for deployment or end-user use.
  - `src/`: For reusable modules, libraries, or shared code. Place code here if it will be imported by multiple scripts or if you want to build a package.
  - `tests/`: For unit and integration tests. Use this folder to store all test code, keeping it separate from production and development scripts.
- Keep related resources (data, configs) in dedicated subfolders as needed.

## 3. Package Management with UV
- Use [UV](https://github.com/astral-sh/uv) for dependency management:
  - Add dependencies with `uv pip install <package>`.
  - Update `pyproject.toml` and `uv.lock` accordingly.
  - Never commit `.venv` or other virtual environment folders.
- Document required dependencies in `pyproject.toml`.

## 4. Coding Standards (PEP8)
- Follow [PEP8](https://peps.python.org/pep-0008/) for code style:
  - 4 spaces per indentation level.
  - Limit lines to 79 characters.
  - Use blank lines to separate functions/classes.
  - Use `snake_case` for variables and functions, `CamelCase` for classes.
  - Add docstrings to all public modules, functions, classes, and methods.
  - Use `isort` and `black` for import and code formatting.

## 5. Execution & Shebang
- Add a shebang line at the top: `#!/usr/bin/env python3` (optional on Windows, but good practice).
- Make scripts executable from the command line: `python main.py`.

## 6. Linting & Formatting
- Use `flake8` or `ruff` for linting.
- Use `black` for code formatting.
- Run `uv pip install black ruff` to add these tools.

## 7. Documentation
- Maintain a `README.md` with usage instructions and script descriptions.
- Comment complex logic and document all public APIs.

## 8. Version Control
- Use `.gitignore` to exclude `.venv/`, `__pycache__/`, and other generated files.
- Commit `pyproject.toml` and `uv.lock` for reproducible environments.

---

**Example Script Skeleton:**

```python
#!/usr/bin/env python3
"""
script_name.py
Description: Brief description of what the script does.
Author: Your Name
"""

import sys
# ...other imports...

def main() -> None:
    # ...main logic...
    pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

---

**References:**
- [PEP8](https://peps.python.org/pep-0008/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Black](https://black.readthedocs.io/en/stable/)
- [Ruff](https://docs.astral.sh/ruff/)
