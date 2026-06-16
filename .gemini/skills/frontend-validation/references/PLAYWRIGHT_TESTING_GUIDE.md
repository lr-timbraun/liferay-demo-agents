# Guide: Interactive Frontend Validation with Playwright

This guide provides patterns for writing Python/Playwright scripts that perform end-to-end demo validation. Unlike headless scraping, these scripts simulate a real user's path through the frontend.

## Core Principles
- **In-Session Continuity:** Perform the entire use case (Login -> Navigation -> Action) in a single browser context to maintain authentication and state.
- **In-Flow Screenshots:** Capture screenshots immediately after significant interactions (e.g., after a hover animation or a successful form submission).
- **Persona Context:** Always use the specific demo credentials defined in the `.env` or the test spec.

## Implementation Pattern (Python)

```python
import asyncio
from playwright.async_api import async_playwright
import os

async def validate_use_case(url, email, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # Runs in background but simulates full UI
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        # 1. Authentication
        print("Performing Login...")
        await page.goto(url + "/c/portal/login")
        await page.fill('input[name="_com_liferay_login_web_portlet_LoginPortlet_login"]', email)
        await page.fill('input[name="_com_liferay_login_web_portlet_LoginPortlet_password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")

        # 2. Capture Authenticated State
        await page.screenshot(path="screenshots/01_logged_in.png")

        # 3. Perform Interaction (e.g., Navigate to a custom object page)
        print("Navigating to use case...")
        await page.goto(url + "/group/guest/my-use-case")
        
        # Verify Visual Element (e.g., a custom fragment)
        await page.wait_for_selector(".my-custom-fragment")
        await page.hover(".my-custom-fragment .card") # Trigger hover state
        await page.screenshot(path="screenshots/02_hover_interaction.png")

        # 4. Data Change Validation
        # (Example: Filling a form fragment)
        await page.fill(".form-fragment input", "Demo Data")
        await page.click(".form-fragment button[type='submit']")
        
        # Capture Success
        await page.wait_for_selector(".alert-success")
        await page.screenshot(path="screenshots/03_form_success.png")

        await browser.close()
```

## Validation Checklist
- **Visuals:** Does the screenshot show the correct brand colors and typography (Classic theme tokens)?
- **Interactions:** Did the hover animation or popup trigger correctly?
- **Data:** If a form was submitted, does the success message appear, and can you verify the new entry via API or a separate UI check?
- **Workflow:** If this is a multi-user test, did the second user see the changes made by the first?
