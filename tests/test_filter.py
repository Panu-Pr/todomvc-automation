"""TS-06 Filters: All / Active / Completed"""

import re

import pytest
from playwright.sync_api import expect

from index import TodoPage


@pytest.fixture
def one_completed(three_todos: TodoPage) -> TodoPage:
    """Three todos with "pay bills" completed."""
    three_todos.toggle(1)
    return three_todos


@pytest.mark.high
def test_tc26_filter_active(one_completed: TodoPage):
    """TC-26: Active filter

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid | Priority: High
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Steps:
        1. Click "Active"
    Expected: Only the 2 active todos are shown; URL ends with #/active
    """
    one_completed.select_filter("Active")

    one_completed.expect_titles("buy milk", "walk dog")
    expect(one_completed.page).to_have_url(re.compile(r"#/active$"))


@pytest.mark.high
def test_tc27_filter_completed(one_completed: TodoPage):
    """TC-27: Completed filter

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Steps:
        1. Click "Completed"
    Expected: Only "pay bills" is shown; URL ends with #/completed
    """
    one_completed.select_filter("Completed")

    one_completed.expect_titles("pay bills")
    expect(one_completed.page).to_have_url(re.compile(r"#/completed$"))


@pytest.mark.med
def test_tc28_back_to_all(one_completed: TodoPage):
    """TC-28: Back to All

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Steps:
        1. Click "Completed"
        2. Click "All"
    Expected: All 3 todos are shown
    """
    one_completed.select_filter("Completed")

    one_completed.select_filter("All")

    one_completed.expect_titles("buy milk", "pay bills", "walk dog")


@pytest.mark.low
@pytest.mark.parametrize("name", ["All", "Active", "Completed"])
def test_tc29_selected_filter_highlighted(one_completed: TodoPage, name: str):
    """TC-29: Selected filter is highlighted

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Test data: All, Active, Completed
    Steps:
        1. Click each filter in turn
    Expected: Only the selected link is highlighted
    """
    one_completed.select_filter(name)

    selected = re.compile(r"(^|\s)selected(\s|$)")
    for other in ["All", "Active", "Completed"]:
        link = expect(one_completed.loc.filter_link(other))
        if other == name:
            link.to_have_class(selected)
        else:
            link.not_to_have_class(selected)


@pytest.mark.med
def test_tc30_browser_back_button(one_completed: TodoPage):
    """TC-30: Browser Back button

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Steps:
        1. Click All → Active → Completed
        2. Press Back twice
    Expected: Each Back returns to the previous filter's view
    """
    one_completed.select_filter("All")
    one_completed.select_filter("Active")
    one_completed.select_filter("Completed")
    one_completed.expect_titles("pay bills")

    one_completed.page.go_back()
    one_completed.expect_titles("buy milk", "walk dog")

    one_completed.page.go_back()
    one_completed.expect_titles("buy milk", "pay bills", "walk dog")


@pytest.mark.med
def test_tc31_open_filter_url_directly(one_completed: TodoPage):
    """TC-31: Open a filter URL directly

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Valid
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Test data: #/active
    Steps:
        1. Open #/active
        2. Reload
    Expected: Only active todos are shown
    """
    one_completed.open("active")
    one_completed.reload()

    one_completed.expect_titles("buy milk", "walk dog")


@pytest.mark.med
def test_tc32_complete_item_while_on_active(one_completed: TodoPage):
    """TC-32: Complete a todo while on Active

    Scenario: TS-06 Filters (All / Active / Completed) | Type: Edge
    Precondition: Page with 3 todos: "buy milk", "pay bills", "walk dog"; "pay bills" completed
    Steps:
        1. Click "Active"
        2. Tick the first todo
    Expected: It disappears; only "walk dog" is shown
    """
    one_completed.select_filter("Active")

    one_completed.toggle(0)

    one_completed.expect_titles("walk dog")
