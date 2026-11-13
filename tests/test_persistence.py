"""TS-07 Persistence (localStorage)"""

import pytest

from index import TodoPage


@pytest.mark.high
def test_tc33_data_survives_reload(todo: TodoPage):
    """TC-33: Data survives a reload

    Scenario: TS-07 Persistence (localStorage) | Type: Valid
    Precondition: Page with 2 todos
    Test data: buy milk, pay bills
    Steps:
        1. Complete the first
        2. Reload
    Expected: Text and status are the same as before the reload
    """
    todo.add("buy milk", "pay bills")
    todo.toggle(0)

    todo.reload()

    todo.expect_titles("buy milk", "pay bills")
    todo.expect_completed(0)
    todo.expect_completed(1, False)


@pytest.mark.med
def test_tc34_local_storage_matches_screen(three_todos: TodoPage):
    """TC-34: localStorage matches the screen

    Scenario: TS-07 Persistence (localStorage) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: walk cat
    Steps:
        1. Complete the 1st todo
        2. Edit the 3rd todo
        3. Read localStorage
    Expected: localStorage holds the same titles and completed flags as the screen
    """
    three_todos.toggle(0)
    three_todos.edit(2, "walk cat")
    three_todos.expect_titles("buy milk", "pay bills", "walk cat")

    stored = [(t["title"], t["completed"]) for t in three_todos.stored_todos()]

    assert stored == [("buy milk", True), ("pay bills", False), ("walk cat", False)]


@pytest.mark.med
def test_tc35_delete_and_edit_survive_reload(three_todos: TodoPage):
    """TC-35: Deletes and edits survive a reload

    Scenario: TS-07 Persistence (localStorage) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: pay rent
    Steps:
        1. Delete the 1st todo
        2. Edit the new 1st todo
        3. Reload
    Expected: The latest values are shown; the deleted todo does not come back
    """
    three_todos.delete(0)
    three_todos.edit(0, "pay rent")

    three_todos.reload()

    three_todos.expect_titles("pay rent", "walk dog")
