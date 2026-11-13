"""TS-02 Complete todos"""

import pytest
from playwright.sync_api import expect

from index import TodoPage


@pytest.mark.high
def test_tc10_mark_todo_as_completed(todo: TodoPage):
    """TC-10: Mark a todo as completed

    Scenario: TS-02 Complete todos | Type: Valid
    Precondition: Page with 2 todos: "buy milk", "pay bills"
    Steps:
        1. Tick the first todo
    Expected: The first is completed (struck through), the second is not; the counter shows "1 item left"
    """
    todo.add("buy milk", "pay bills")

    todo.toggle(0)

    todo.expect_completed(0)
    todo.expect_completed(1, False)
    todo.expect_count_text("1 item left")


@pytest.mark.high
def test_tc11_unmark_completed_todo(todo: TodoPage):
    """TC-11: Unmark a completed todo

    Scenario: TS-02 Complete todos | Type: Valid
    Precondition: Page with 2 todos, the first completed
    Steps:
        1. Click the first todo's checkbox again
    Expected: Back to active; the counter shows "2 items left"
    """
    todo.add("buy milk", "pay bills")
    todo.toggle(0)

    todo.toggle(0)

    todo.expect_completed(0, False)
    todo.expect_count_text("2 items left")


@pytest.mark.high
def test_tc12_mark_all_as_completed(three_todos: TodoPage):
    """TC-12: Mark all as complete

    Scenario: TS-02 Complete todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Click "Mark all as complete"
    Expected: All completed; the counter shows "0 items left"
    """
    three_todos.loc.toggle_all.check()

    for i in range(3):
        three_todos.expect_completed(i)
    three_todos.expect_count_text("0 items left")


@pytest.mark.med
def test_tc13_unmark_all(three_todos: TodoPage):
    """TC-13: Unmark all

    Scenario: TS-02 Complete todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; all completed
    Steps:
        1. Click "Mark all as complete" again
    Expected: All back to active; the counter shows "3 items left"
    """
    three_todos.loc.toggle_all.check()

    three_todos.loc.toggle_all.uncheck()

    for i in range(3):
        three_todos.expect_completed(i, False)
    three_todos.expect_count_text("3 items left")


@pytest.mark.med
def test_tc14_toggle_all_follows_items(three_todos: TodoPage):
    """TC-14: Toggle-all follows the items

    Scenario: TS-02 Complete todos | Type: Edge
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Tick every todo one by one
        2. Untick one
    Expected: Toggle-all is checked when all are done and unchecked after one is unticked
    """
    for i in range(3):
        three_todos.toggle(i)
    expect(three_todos.loc.toggle_all).to_be_checked()

    three_todos.toggle(0)

    expect(three_todos.loc.toggle_all).not_to_be_checked()
