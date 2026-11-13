# TodoMVC Automation Tests

Automated UI tests for [React • TodoMVC](https://demo.playwright.dev/todomvc/#/), written in **Python + Pytest + Playwright** using the **Page Object Model**.

- All test cases (35, TC-01 to TC-35): [docs/TEST_CASES.xlsx](docs/TEST_CASES.xlsx) (Excel, with precondition, type, test data and the automated test for each case) and [docs/TEST_CASES.md](docs/TEST_CASES.md) (readable on GitHub)
- Every test name starts with its TC ID (e.g. `test_tc01_add_one_todo`), so code and documentation trace to each other.

## Setup until runnable

### 1. Prerequisites

| Tool | Version | Check with |
| --- | --- | --- |
| Python | 3.10 or later | `python --version` (on macOS/Linux this may be `python3`) |
| Git | any | `git --version` |

No Python yet? Download it from https://www.python.org/downloads/ (on Windows, tick **Add python.exe to PATH** during install).

### 2. Clone and create a virtual environment

```bash
git clone <repo-url>
cd todomvc-automation
python -m venv .venv
```

Activate the virtual environment:

| OS | Command |
| --- | --- |
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |

> If PowerShell says scripts are disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

### 3. Install libraries and the browser

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

On Linux without the system libraries a browser needs, use `python -m playwright install --with-deps chromium`.

| Library | Purpose |
| --- | --- |
| `pytest` | Test runner |
| `playwright` | Browser automation |
| `pytest-playwright` | Connects Playwright to pytest (`page` fixture, `--browser`, `--headed`, screenshots, traces) |
| `pytest-html` | HTML report |

### 4. Run the tests

```bash
pytest
```

Expected result: `38 passed` (35 test cases; TC-04 runs with 2 data sets and TC-29 with 3).

## Common commands

| Goal | Command |
| --- | --- |
| Run everything | `pytest` |
| Watch the browser | `pytest --headed --slowmo 300` |
| High priority only (smoke) | `pytest -m high` |
| One scenario | `pytest tests/test_edit.py` |
| One test case | `pytest -k tc15` |
| Another browser | `pytest --browser firefox` (run `python -m playwright install firefox` first) |
| Run in parallel | `pip install pytest-xdist`, then `pytest -n auto` |
| Point at another environment | `pytest --base-url https://staging.example.com/todomvc/` |

## Output

| Path | Contents |
| --- | --- |
| `reports/report.html` | HTML report of the latest run; open it in a browser |
| `test-results/` | Screenshots and traces of failed tests only |

Open the trace of a failed test to replay it step by step (DOM, network, console):

```bash
python -m playwright show-trace test-results/<test-name>/trace.zip
```

## Structure

```
.
├── pages/                      # Page Objects: everything that knows the web page
│   ├── todo_locators.py        # How to find every element on the Todo page
│   └── todo_page.py            # Actions on the Todo page (add, complete, edit, delete, filter)
├── data/
│   └── todo_data.py            # Test data
├── index.py                    # Single entry point: tests import everything from here
├── tests/                      # Tests, one file per scenario
│   ├── conftest.py             # Fixtures: fresh page per test, starting data
│   ├── test_add.py             # TS-01 Add todos
│   ├── test_complete.py        # TS-02 Complete todos
│   ├── test_edit.py            # TS-03 Edit todos
│   ├── test_delete.py          # TS-04 Delete todos
│   ├── test_counter.py         # TS-05 Item counter
│   ├── test_filter.py          # TS-06 Filters
│   └── test_persistence.py     # TS-07 Persistence
├── docs/
│   ├── TEST_CASES.xlsx         # Test cases (Excel)
│   └── TEST_CASES.md           # Same test cases, readable on GitHub
├── .github/workflows/tests.yml # CI: runs on every push and keeps the report
├── pytest.ini                  # Base URL, markers, report options
└── requirements.txt
```

### How the layers connect

```
tests/test_*.py ──import──▶ index.py (entry point)
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
             pages/todo_page.py   data/todo_data.py
                     │
                     ▼
           pages/todo_locators.py
```

- **index** gathers every part in one place. Tests only write `from index import TodoData, TodoPage` and never need to know which file holds what.
- **tests** call page actions and take values from data. Test files contain no selectors (the text or IDs used to find elements).
- **page** knows what to do on the page (e.g. adding a todo = type, then press Enter) but not where elements are; it asks the locators.
- **locators** know only where each element is.

Locators and actions for the same page live together in `pages/` but in separate files, because a page change usually means looking at both. Each file has exactly one reason to change:

| What changed | Edit |
| --- | --- |
| The page's look or HTML | `pages/todo_locators.py` |
| How the page is used | `pages/todo_page.py` |
| Test data | `data/todo_data.py` |
| Site or environment under test | `pytest.ini` or `--base-url` |
| What should be verified | `tests/` |

### Design principles

- **Page Object Model with separate locators:** all selectors live in `pages/todo_locators.py`. When the page changes, one file changes and tests stay untouched.
- **Resilient locators:** placeholder, label, role and `data-testid` instead of layout-bound XPath (CSS classes only for `.main` / `.footer`, where nothing else exists).
- **Independent tests:** pytest-playwright creates a new browser context per test (empty localStorage), so tests can run in any order or in parallel.
- **No sleeps:** Playwright's `expect()` waits until the condition holds, which keeps tests from being flaky.
- **Grouped by scenario and priority:** one file per scenario, plus `high` / `med` / `low` markers to run subsets.
- **One place for settings:** base URL and run options live in `pytest.ini`; switch environments with `--base-url` without touching code.
- **Evidence on failure:** screenshots and traces are kept automatically.
- **CI:** GitHub Actions runs the suite on every push and attaches the report for download.

## Adding tests

**A new test on an existing page**

1. Add the test case to `docs/TEST_CASES.xlsx` and `docs/TEST_CASES.md` with the next ID (e.g. TC-36).
2. If it needs new data, add it to `data/todo_data.py`.
3. Write the test in that scenario's file, name it `test_tc36_<what_it_checks>` and add a priority marker.
4. If it needs an action that doesn't exist yet, add a method to `pages/todo_page.py`.

**A new page** (e.g. login)

1. `pages/login_locators.py`: that page's locators.
2. `pages/login_page.py`: that page's actions, using the locators from step 1.
3. Add an import line to `index.py`.
4. Add a fixture to `tests/conftest.py` and write tests under `tests/`.

## Notes

- The challenge gives no requirements for the site, so expected behaviour follows the [TodoMVC App Specification](https://github.com/tastejs/todomvc/blob/master/app-spec.md).
- The app stores data in the browser's localStorage and has no backend, so persistence is verified directly against localStorage (TC-34).
