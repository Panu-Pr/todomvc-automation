"""Test data.

Kept apart from the tests so data can change without touching test steps.
"""


class TodoData:
    # Starting todos
    ONE = "buy milk"
    THREE = ("buy milk", "pay bills", "walk dog")

    # Text used when editing
    EDITED = "pay rent"

    # Special input (the Thai text is intentional: it checks non-Latin characters)
    WITH_SPACES = "   buy milk   "
    BLANKS = ("", "     ")
    THAI_EMOJI_SPECIAL = "ซื้อนม 🥛 & <b>bread</b>"
    HTML_INJECTION = "<img src=x onerror=alert(1)>"
    LONG = "a" * 500
