"""TS-04 Delete todos"""

import pytest
from playwright.sync_api import expect

from index import TodoData, TodoPage


@pytest.mark.high
def test_tc21_delete_with_button(three_todos: TodoPage):
    """TC-21: Delete with the × button

    Scenario: TS-04 Delete todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Hover the 2nd todo
        2. Click ×
    Expected: The todo is gone; the counter shows "2 items left"
    """
    three_todos.delete(1)

    three_todos.expect_titles("buy milk", "walk dog")
    three_todos.expect_count_text("2 items left")


@pytest.mark.high
def test_tc22_clear_completed_removes_only_completed(three_todos: TodoPage):
    """TC-22: Clear completed

    Scenario: TS-04 Delete todos | Type: Valid | Priority: High
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Complete the 1st and 3rd todos
        2. Click "Clear completed"
    Expected: Only "pay bills" remains
    """
    three_todos.toggle(0)
    three_todos.toggle(2)

    three_todos.clear_completed()

    three_todos.expect_titles("pay bills")


@pytest.mark.low
def test_tc23_clear_completed_shown_only_when_any_completed(three_todos: TodoPage):
    """TC-23: "Clear completed" shown only when needed

    Scenario: TS-04 Delete todos | Type: Valid | Priority: Low
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Check the button
        2. Complete a todo
        3. Check again
    Expected: Hidden with no completed todos, shown with at least one
    """
    expect(three_todos.loc.clear_completed).to_be_hidden()

    three_todos.toggle(0)

    expect(three_todos.loc.clear_completed).to_be_visible()


@pytest.mark.med
def test_tc24_delete_last_todo_hides_main_and_footer(todo: TodoPage):
    """TC-24: Delete the last todo

    Scenario: TS-04 Delete todos | Type: Edge | Priority: Med
    Precondition: Page with 1 todo
    Test data: buy milk
    Steps:
        1. Delete the todo
    Expected: No todos; the list and footer are hidden
    """
    todo.add(TodoData.ONE)

    todo.delete(0)

    expect(todo.loc.items).to_have_count(0)
    expect(todo.loc.main).to_be_hidden()
    expect(todo.loc.footer).to_be_hidden()
