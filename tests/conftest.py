import pytest
from playwright.sync_api import Page

from index import TodoData, TodoPage


@pytest.fixture
def todo(page: Page) -> TodoPage:
    """A freshly opened TodoMVC page for every test.

    pytest-playwright creates a new browser context per test, so localStorage
    always starts empty and tests never affect each other.
    """
    return TodoPage(page).open()


@pytest.fixture
def three_todos(todo: TodoPage) -> TodoPage:
    """A page that already has three todos."""
    todo.add(*TodoData.THREE)
    return todo
