"""Locators for the TodoMVC page.

The only place that knows how to find elements. If the page markup changes,
only this file changes.

Preferred order:
1. What the user sees: placeholder, label, role + accessible name
2. data-testid attributes added for testing
3. CSS classes (only when nothing else is available)
"""

from playwright.sync_api import Locator, Page


class TodoLocators:
    def __init__(self, page: Page):
        self.page = page

        # Header
        self.new_todo = page.get_by_placeholder("What needs to be done?")

        # List
        self.main = page.locator(".main")
        self.toggle_all = page.get_by_label("Mark all as complete")
        self.items = page.get_by_test_id("todo-item")
        self.titles = page.get_by_test_id("todo-title")

        # Footer
        self.footer = page.locator(".footer")
        self.counter = page.get_by_test_id("todo-count")
        self.clear_completed = page.get_by_role("button", name="Clear completed")

    def filter_link(self, name: str) -> Locator:
        """Filter link. name = "All" | "Active" | "Completed" """
        return self.page.get_by_role("link", name=name, exact=True)

    # ----- Elements inside a single todo (by index) -----
    def item(self, index: int) -> Locator:
        return self.items.nth(index)

    def item_checkbox(self, index: int) -> Locator:
        return self.item(index).get_by_role("checkbox")

    def item_editor(self, index: int) -> Locator:
        return self.item(index).get_by_role("textbox", name="Edit")

    def item_delete_button(self, index: int) -> Locator:
        return self.item(index).get_by_role("button", name="Delete")
