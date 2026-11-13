# Test Cases: TodoMVC (React)

Site under test: https://demo.playwright.dev/todomvc/#/
The challenge gives no requirements, so expected behaviour follows the [TodoMVC App Specification](https://github.com/tastejs/todomvc/blob/master/app-spec.md).

Every test case is automated. Each TC ID matches a test name in the code (e.g. `test_tc01_...`) for traceability.

**Priority:** High = core function; if broken, the app is unusable / Med = works but wrong in some cases / Low = convenience or display

**Precondition for all cases:** a freshly opened page (empty localStorage) unless stated otherwise.

## TS-01 Add todos

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-01 | Add one todo | Type "buy milk" and press Enter | The list shows "buy milk", the input is cleared, the counter shows "1 item left" | High |
| TC-02 | Add several todos | Add 3 todos in order | All 3 are shown in the order added; the counter shows "3 items left" | High |
| TC-03 | Trim leading and trailing spaces | Add "&nbsp;&nbsp;buy milk&nbsp;&nbsp;" | The todo is saved as "buy milk" | Med |
| TC-04 | Empty or blank input | Press Enter with an empty input, then with spaces only | No todo is added | High |
| TC-05 | Thai text, emoji and special characters | Add "ซื้อนม 🥛 & <b>bread</b>" | Shown exactly as typed (`<b>` stays text, not bold) | Med |
| TC-06 | HTML / script injection | Add `<img src=x onerror=alert(1)>` | Shown as text; no dialog appears | Med |
| TC-07 | Very long text | Add a 500-character todo | Added, and the full text is stored | Low |
| TC-08 | Duplicate text | Add "buy milk" twice | Two todos; the counter shows "2 items left" | Low |
| TC-09 | List and footer appear only with todos | Check the page before and after adding the first todo | Hidden before, shown after | Med |

## TS-02 Complete todos

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-10 | Mark a todo as completed | With 2 todos, tick the first | The first is completed (struck through); the counter shows "1 item left" | High |
| TC-11 | Unmark a completed todo | Tick, then click again | Back to active; the counter goes back up | High |
| TC-12 | Mark all as complete | With 3 todos, click the toggle-all control | All completed; the counter shows "0 items left" | High |
| TC-13 | Unmark all | With all completed, click toggle-all again | All back to active | Med |
| TC-14 | Toggle-all follows the items | Tick every todo one by one, then untick one | Toggle-all is checked when all are done and unchecked after one is unticked | Med |

## TS-03 Edit todos

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-15 | Edit and press Enter | Double-click a todo, change the text, press Enter | The new text is saved | High |
| TC-16 | Edit and click away (blur) | Double-click, change the text, click outside | The new text is saved | Med |
| TC-17 | Trim spaces when editing | Change the text to "&nbsp;&nbsp;new text&nbsp;&nbsp;" | Saved as "new text" | Med |
| TC-18 | Edit to empty | Clear the text and press Enter | The todo is removed | Med |
| TC-19 | Escape cancels editing | Change the text, then press Escape | The original text is kept | Med |
| TC-20 | Controls hidden while editing | Double-click a todo | Its checkbox and delete button are hidden | Low |

## TS-04 Delete todos

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-21 | Delete with the × button | Hover a todo and click × | The todo is gone; the counter updates | High |
| TC-22 | Clear completed | With 3 todos, complete 2, click "Clear completed" | Only the active todo remains | High |
| TC-23 | "Clear completed" shown only when needed | Check the button before and after completing a todo | Hidden with no completed todos, shown with at least one | Low |
| TC-24 | Delete the last todo | With 1 todo, delete it | The list and footer are hidden | Med |

## TS-05 Item counter

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-25 | Singular and plural | Change the number of active todos to 2, 1, 0 | "2 items left", "1 item left", "0 items left" | Low |

## TS-06 Filters (All / Active / Completed)

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-26 | Active filter | With 3 todos, 1 completed, click "Active" | Only the 2 active todos are shown; URL ends with #/active | High |
| TC-27 | Completed filter | As TC-26, then click "Completed" | Only the completed todo is shown; URL ends with #/completed | High |
| TC-28 | Back to All | From Completed, click "All" | All 3 todos are shown | Med |
| TC-29 | Selected filter is highlighted | Click each filter | Only the selected link is highlighted | Low |
| TC-30 | Browser Back button | Click All → Active → Completed, then press Back | Returns to the previous filters in order | Med |
| TC-31 | Open a filter URL directly | With data, open #/active directly | Only active todos are shown | Med |
| TC-32 | Complete a todo while on Active | On Active, tick a todo | It disappears from the Active view | Med |

## TS-07 Persistence (localStorage)

| ID | Test case | Steps | Expected result | Priority |
| --- | --- | --- | --- | --- |
| TC-33 | Data survives a reload | Add 2 todos, complete 1, reload | Text and status are the same as before | High |
| TC-34 | localStorage matches the screen | Add, complete and edit todos | localStorage holds the same titles and completed flags as the screen | Med |
| TC-35 | Deletes and edits survive a reload | Delete 1 todo, edit 1, reload | The latest values are shown; the deleted todo does not come back | Med |

## Summary

| Scenario | Total | High | Med | Low |
| --- | --- | --- | --- | --- |
| TS-01 Add todos | 9 | 3 | 4 | 2 |
| TS-02 Complete todos | 5 | 3 | 2 | 0 |
| TS-03 Edit todos | 6 | 1 | 4 | 1 |
| TS-04 Delete todos | 4 | 2 | 1 | 1 |
| TS-05 Item counter | 1 | 0 | 0 | 1 |
| TS-06 Filters | 7 | 2 | 4 | 1 |
| TS-07 Persistence | 3 | 1 | 2 | 0 |
| **Total** | **35** | **12** | **17** | **6** |

**Out of scope:** load testing; server-side security (the app stores data only in the browser and has no backend); browsers other than Chromium (supported via pytest-playwright's `--browser` option).
