"""This single entry file ties every part of the suite together.

Tests import from here only, so they never depend on where each part lives.

    from index import TodoData, TodoPage

| Part      | File                    | Role                                    |
| --------- | ----------------------- | --------------------------------------- |
| locators  | pages/todo_locators.py  | How to find every element on the page   |
| pages     | pages/todo_page.py      | Actions on the page (uses the locators) |
| data      | data/todo_data.py       | Test data                               |

New page: add its locators + page under pages/, then add an import line below.
"""

from data.todo_data import TodoData
from pages.todo_locators import TodoLocators
from pages.todo_page import TodoPage

__all__ = ["TodoData", "TodoLocators", "TodoPage"]
