"""TS-01 Add todos"""

import pytest
from playwright.sync_api import Dialog, expect

from index import TodoData, TodoPage


@pytest.mark.high
def test_tc01_add_one_todo(todo: TodoPage):
    """TC-01: Add one todo

    Scenario: TS-01 Add todos | Type: Valid
    Precondition: Fresh page (empty localStorage)
    Test data: buy milk
    Steps:
        1. Type a todo
        2. Press Enter
    Expected: The list shows "buy milk", the input is cleared, the counter shows "1 item left"
    """
    todo.add(TodoData.ONE)

    todo.expect_titles(TodoData.ONE)
    expect(todo.loc.new_todo).to_be_empty()
    todo.expect_count_text("1 item left")


@pytest.mark.high
def test_tc02_add_multiple_todos_in_order(todo: TodoPage):
    """TC-02: Add several todos

    Scenario: TS-01 Add todos | Type: Valid
    Precondition: Fresh page (empty localStorage)
    Test data: buy milk, pay bills, walk dog
    Steps:
        1. Add 3 todos in order
    Expected: All 3 are shown in the order added; the counter shows "3 items left"
    """
    todo.add(*TodoData.THREE)

    todo.expect_titles(*TodoData.THREE)
    todo.expect_count_text("3 items left")


@pytest.mark.med
def test_tc03_trim_whitespace_on_add(todo: TodoPage):
    """TC-03: Trim leading and trailing spaces

    Scenario: TS-01 Add todos | Type: Edge
    Precondition: Fresh page (empty localStorage)
    Test data: "   buy milk   "
    Steps:
        1. Add a todo with spaces around it
    Expected: The todo is shown and stored as "buy milk"
    """
    todo.add(TodoData.WITH_SPACES)

    expect(todo.loc.titles).to_have_text([TodoData.ONE], use_inner_text=True)
    assert todo.stored_todos()[0]["title"] == TodoData.ONE


@pytest.mark.high
@pytest.mark.parametrize("text", TodoData.BLANKS, ids=["empty", "spaces-only"])
def test_tc04_empty_or_blank_is_not_added(todo: TodoPage, text: str):
    """TC-04: Empty or blank input

    Scenario: TS-01 Add todos | Type: Invalid
    Precondition: Fresh page (empty localStorage)
    Test data: "", "     "
    Steps:
        1. Press Enter with an empty input
        2. Press Enter with spaces only
    Expected: No todo is added
    """
    todo.add(text)

    expect(todo.loc.items).to_have_count(0)


@pytest.mark.med
def test_tc05_thai_emoji_and_special_characters(todo: TodoPage):
    """TC-05: Thai text, emoji and special characters

    Scenario: TS-01 Add todos | Type: Valid
    Precondition: Fresh page (empty localStorage)
    Test data: ซื้อนม 🥛 & <b>bread</b>
    Steps:
        1. Add the todo
    Expected: Shown exactly as typed; <b> stays text, not bold
    """
    text = TodoData.THAI_EMOJI_SPECIAL
    todo.add(text)

    todo.expect_titles(text)
    expect(todo.loc.item(0).locator("b")).to_have_count(0)


@pytest.mark.med
def test_tc06_html_is_not_executed(todo: TodoPage):
    """TC-06: HTML / script injection

    Scenario: TS-01 Add todos | Type: Invalid
    Precondition: Fresh page (empty localStorage)
    Test data: <img src=x onerror=alert(1)>
    Steps:
        1. Add the todo
    Expected: Shown as text; no image element and no dialog
    """
    dialogs: list[Dialog] = []
    todo.page.on("dialog", lambda d: (dialogs.append(d), d.dismiss()))
    payload = TodoData.HTML_INJECTION

    todo.add(payload)

    todo.expect_titles(payload)
    expect(todo.loc.item(0).locator("img")).to_have_count(0)
    assert dialogs == []


@pytest.mark.low
def test_tc07_very_long_text(todo: TodoPage):
    """TC-07: Very long text

    Scenario: TS-01 Add todos | Type: Edge
    Precondition: Fresh page (empty localStorage)
    Test data: 500 characters
    Steps:
        1. Add the todo
    Expected: Added, and the full text is stored
    """
    text = TodoData.LONG
    todo.add(text)

    todo.expect_titles(text)
    assert todo.stored_todos()[0]["title"] == text


@pytest.mark.low
def test_tc08_duplicate_text_allowed(todo: TodoPage):
    """TC-08: Duplicate text

    Scenario: TS-01 Add todos | Type: Edge
    Precondition: Fresh page (empty localStorage)
    Test data: buy milk ×2
    Steps:
        1. Add the same todo twice
    Expected: Two todos; the counter shows "2 items left"
    """
    todo.add(TodoData.ONE, TodoData.ONE)

    todo.expect_titles(TodoData.ONE, TodoData.ONE)
    todo.expect_count_text("2 items left")


@pytest.mark.med
def test_tc09_main_and_footer_shown_only_with_todos(todo: TodoPage):
    """TC-09: List and footer appear only with todos

    Scenario: TS-01 Add todos | Type: Valid
    Precondition: Fresh page (empty localStorage)
    Test data: buy milk
    Steps:
        1. Check the page
        2. Add the first todo
        3. Check again
    Expected: Hidden before, shown after
    """
    expect(todo.loc.main).to_be_hidden()
    expect(todo.loc.footer).to_be_hidden()

    todo.add(TodoData.ONE)

    expect(todo.loc.main).to_be_visible()
    expect(todo.loc.footer).to_be_visible()
