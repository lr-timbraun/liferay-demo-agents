---
name: playwright-scraper
description: Headless browser automation for DOM extraction using Playwright. Use when standard web fetching fails to capture JavaScript-rendered content for fragment analysis.
---

# Skill: Playwright Scraper

## Description
This skill provides the procedural knowledge for using Playwright to extract full, rendered DOMs from modern, dynamic websites.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write Playwright scripts from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating any Python scraping scripts:

- **Playwright Setup & Scripts**: Read **[PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md](references/PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md)** to obtain the validated installation commands and the correct `get_dom.py` implementation logic.

## Supplemental Guidance

### 1. Implementation: Headless Browsing
- **Chromium instances:** Launch Chromium instances to execute client-side JavaScript.
- **Rendered HTML Capture:** Navigate to URLs and wait for `domcontentloaded` to capture the final state of a page.

### 2. Implementation: Usage
- **Fragment Analysis Preparation:** Save full DOM extractions to enable accurate analysis for fragment creation.
- **Execution:** Run the scraper script: `python scripts/get_dom.py <URL> --output <filename>.html`

## Validation Phase
- **Integrity Check:** Confirm that the output file exists in the `input/` directory and contains the expected content.

## Available Resources
- Scraper Script: `scripts/get_dom.py`
- Reference: Playwright Guide: `references/PLAYWRIGHT_GUIDE_DOM_EXTRACTION.md`
