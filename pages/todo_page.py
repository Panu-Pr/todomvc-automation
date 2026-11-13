"""Page Object for the TodoMVC page.

Actions a user can take (add, complete, edit, delete, filter), built on the
locators in pages/todo_locators.py. Tests call these methods and only assert.
"""

import json
import re

from playwright.sync_api import Page, expect

from pages.todo_locators import TodoLocators

# localStorage key the TodoMVC (React) app stores todos under
STORAGE_KEY = "react-todos"


class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.loc = TodoLocators(page)

    # ---------- navigation ----------
    def open(self, route: str = "") -> "TodoPage":
        """Open the app. route = "" | "active" | "completed" (relative to base_url in pytest.ini)

        Waits for the app to render instead of the full page "load" event, so a slow
        third-party resource on the demo site cannot time out the navigation.
        """
        self.page.goto(f"#/{route}", wait_until="domcontentloaded")
        expect(self.loc.new_todo).to_be_visible()
        return self

    def reload(self) -> None:
        self.page.reload()

    def select_filter(self, name: str) -> None:
        self.loc.filter_link(name).click()

    # ---------- actions ----------
    def add(self, *texts: str) -> None:
        for text in texts:
            self.loc.new_todo.fill(text)
            self.loc.new_todo.press("Enter")

    def toggle(self, index: int) -> None:
        self.loc.item_checkbox(index).click()

    def start_edit(self, index: int) -> None:
        self.loc.item(index).dblclick()

    def edit(self, index: int, text: str, finish_with: str = "Enter") -> None:
        """Edit a todo. finish_with = "Enter" | "Escape" | "blur" """
        self.start_edit(index)
        editor = self.loc.item_editor(index)
        editor.fill(text)
        if finish_with == "blur":
            editor.dispatch_event("blur")
        else:
            editor.press(finish_with)

    def delete(self, index: int) -> None:
        self.loc.item(index).hover()
        self.loc.item_delete_button(index).click()

    def clear_completed(self) -> None:
        self.loc.clear_completed.click()

    # ---------- reads ----------
    def stored_todos(self) -> list[dict]:
        """Todos as stored by the app in localStorage."""
        raw = self.page.evaluate(f"() => localStorage.getItem('{STORAGE_KEY}')")
        return json.loads(raw) if raw else []

    # ---------- common assertions ----------
    def expect_titles(self, *texts: str) -> None:
        expect(self.loc.titles).to_have_text(list(texts))

    def expect_count_text(self, text: str) -> None:
        expect(self.loc.counter).to_have_text(text)

    def expect_completed(self, index: int, completed: bool = True) -> None:
        if completed:
            expect(self.loc.item(index)).to_have_class(has_class("completed"))
        else:
            expect(self.loc.item(index)).not_to_have_class(has_class("completed"))


def has_class(name: str) -> re.Pattern:
    """Regex matching a whole class name (an element may have several classes)."""
    return re.compile(rf"(^|\s){name}(\s|$)")
