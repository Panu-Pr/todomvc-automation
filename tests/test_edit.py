"""TS-03 Edit todos"""

import pytest
from playwright.sync_api import expect

from index import TodoData, TodoPage


@pytest.mark.high
def test_tc15_edit_and_press_enter(three_todos: TodoPage):
    """TC-15: Edit and press Enter

    Scenario: TS-03 Edit todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: pay rent
    Steps:
        1. Double-click the 2nd todo
        2. Change the text
        3. Press Enter
    Expected: The new text is saved; other todos unchanged
    """
    three_todos.edit(1, TodoData.EDITED)

    three_todos.expect_titles("buy milk", TodoData.EDITED, "walk dog")


@pytest.mark.med
def test_tc16_edit_and_blur(three_todos: TodoPage):
    """TC-16: Edit and click away (blur)

    Scenario: TS-03 Edit todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: pay rent
    Steps:
        1. Double-click the 2nd todo
        2. Change the text
        3. Leave the field
    Expected: The new text is saved
    """
    three_todos.edit(1, TodoData.EDITED, finish_with="blur")

    three_todos.expect_titles("buy milk", TodoData.EDITED, "walk dog")


@pytest.mark.med
def test_tc17_trim_whitespace_on_edit(three_todos: TodoPage):
    """TC-17: Trim spaces when editing

    Scenario: TS-03 Edit todos | Type: Edge
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: "   pay rent   "
    Steps:
        1. Double-click the 2nd todo
        2. Enter text with spaces around it
        3. Press Enter
    Expected: Shown and stored as "pay rent"
    """
    three_todos.edit(1, f"   {TodoData.EDITED}   ")

    three_todos.expect_titles("buy milk", TodoData.EDITED, "walk dog")
    assert three_todos.stored_todos()[1]["title"] == TodoData.EDITED


@pytest.mark.med
def test_tc18_edit_to_empty_removes_todo(three_todos: TodoPage):
    """TC-18: Edit to empty

    Scenario: TS-03 Edit todos | Type: Edge
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: ""
    Steps:
        1. Double-click the 2nd todo
        2. Clear the text
        3. Press Enter
    Expected: The todo is removed
    """
    three_todos.edit(1, "")

    three_todos.expect_titles("buy milk", "walk dog")


@pytest.mark.med
def test_tc19_escape_cancels_edit(three_todos: TodoPage):
    """TC-19: Escape cancels editing

    Scenario: TS-03 Edit todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Test data: pay rent
    Steps:
        1. Double-click the 2nd todo
        2. Change the text
        3. Press Escape
    Expected: The original text "pay bills" is kept
    """
    three_todos.edit(1, TodoData.EDITED, finish_with="Escape")

    three_todos.expect_titles("buy milk", "pay bills", "walk dog")


@pytest.mark.low
def test_tc20_controls_hidden_while_editing(three_todos: TodoPage):
    """TC-20: Controls hidden while editing

    Scenario: TS-03 Edit todos | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"
    Steps:
        1. Double-click the 2nd todo
    Expected: Its checkbox and delete button are hidden
    """
    three_todos.start_edit(1)

    expect(three_todos.loc.item_checkbox(1)).to_be_hidden()
    expect(three_todos.loc.item_delete_button(1)).to_be_hidden()
