---
name: frontend-validation
description: Comprehensive, persona-based frontend validation for Liferay demos. Uses Playwright to simulate interactions and capture in-flow screenshots for a final test report.
---

# Skill: Frontend Validation

## Description
This skill provides the procedural knowledge for verifying the **total setup** of a Liferay demo. It involves writing and executing interactive Playwright scripts that perform use cases from the perspective of specific personas, capturing visual and data-driven results.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build validation scripts from memory. You MUST use the `read_file` tool to read the following reference document BEFORE writing any code:

- **Interactive Testing Guide**: Read **[PLAYWRIGHT_TESTING_GUIDE.md](references/PLAYWRIGHT_TESTING_GUIDE.md)** to obtain the Python/Playwright templates for in-session navigation and screenshot capture.

## Supplemental Guidance

### 1. Spec Ingestion
- **Analyze the Test Plan:** Read `specs/TEST_PLAN.md` to identify the target personas, the step-by-step use cases, and the mandatory screenshot checkpoints.

### 2. Implementation: Interactive Scripting
- **Persistent Session:** You MUST use a single browser context for each persona test to maintain authentication and state.
- **Visual Capture:** Use `page.screenshot()` at every checkpoint defined in the test plan. Ensure hovers or animations are active when capturing.
- **Workflow Verification:** If the demo involves a handoff (e.g., Request -> Approval), you MUST script both sides of the interaction using the correct users.

### 3. Test Report Generation
- **Pass/Fail Audit:** For every use case, explicitly state if the result matched the expected outcome.
- **Visual Evidence:** Incorporate the captured screenshots into a root-level `TEST_REPORT_<YYYYMMDD_HHMMSS>.md`.
- **Narrative Context:** Provide a brief description for each screenshot explaining what is being validated (e.g., "Verification of primary button hover state").

## Available Resources
- Playwright Documentation: https://playwright.dev/python/docs/intro
- Reference: Playwright Testing Guide: `references/PLAYWRIGHT_TESTING_GUIDE.md`
