"""TS-05 Item counter"""

import pytest

from index import TodoPage


@pytest.mark.low
def test_tc25_counter_singular_and_plural(todo: TodoPage):
    """TC-25: Singular and plural

    Scenario: TS-05 Item counter | Type: Valid
    Precondition: Page with 2 todos
    Steps:
        1. Check the counter
        2. Complete one
        3. Complete the other
    Expected: "2 items left" → "1 item left" → "0 items left"
    """
    todo.add("buy milk", "pay bills")
    todo.expect_count_text("2 items left")

    todo.toggle(0)
    todo.expect_count_text("1 item left")

    todo.toggle(1)
    todo.expect_count_text("0 items left")
