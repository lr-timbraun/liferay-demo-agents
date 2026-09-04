# Guide: Playwright DOM Extraction & Page Driving

This reference guide provides standard Playwright locator schemas and timing sequences for headlessly driving Liferay DXP.

---

## 1. DXP Administrative Login Sequence

Always log in using standard credentials loaded securely via the `env_utils` library:

```python
from playwright.sync_api import sync_playwright

def login_dxp(page, host, username, password):
    page.goto(f"{host}/web/guest/home")
    # Click sign in if present
    if page.locator("text=Sign In").is_visible():
        page.locator("text=Sign In").click()
    # Fill login form
    page.locator("input[type='email']").fill(username)
    page.locator("input[type='password']").fill(password)
    page.locator("button[type='submit']").click()
    page.wait_for_load_state("networkidle")
```

---

## 2. Overwriting Duplication Modal ("Manage Existing Items")

If an asset (like a Stylebook or fragment set) already exists, DXP pops open an overwrite modal overlay. Handle it cleanly using this language-independent value selector:

```python
def handle_overwrite_modal(page):
    # Wait for duplication modal to appear on-screen
    if page.locator(".modal-dialog").is_visible():
        # Select overwrite radio option
        page.locator("input[value='overwrite']").click()
        # Click the submit/Save button
        page.locator(".modal-footer button:has-text('Save')").click()
        # Wait for dialog and backdrop to fade out completely
        page.locator(".modal-dialog").wait_for(state="hidden")
        page.locator(".modal-backdrop").wait_for(state="hidden")
        page.wait_for_timeout(1000) # safety pause
```
