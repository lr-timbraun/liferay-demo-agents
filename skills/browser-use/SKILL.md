---
name: browser-use
description: Headless browser automation using Playwright to interact with Liferay portals, perform actions like a human, and capture visual receipt screenshots.
---

# Skill: Browser Use (RPA Automation)

## Description
This skill provides implementation guidelines and code snippets for driving headless Chromium sessions to log into Liferay DXP, fill forms, trigger workflow transition actions, and capture high-resolution visual receipts of alert states.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write Playwright automation routes from memory. You MUST load and read these files BEFORE executing any browser-use tasks:
- **Playwright DOM Extraction Guide**: Read **[references/PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md](references/PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md)** to obtain the exact locator strategies and timing sequences.

## Supplemental Guidance

### 1. Robust Wait States
- Never assume an overlay fade-out is immediate.
- Always wait for `.modal-dialog` and `.modal-backdrop` to be completely hidden (`state="hidden"`) with a `1000ms` safety pause before snapping screenshots.

### 2. File Receipt Naming Conventions
Match the standard format strictly:
```
receipt_{resource_type}_{resource_name}_{YYYYMMDD_HHMMSS}_{status}.png
```

## Available Resources
- Playwright DOM Extraction Guide: `references/PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md`
- Core Script: `scripts/get_dom.py`
