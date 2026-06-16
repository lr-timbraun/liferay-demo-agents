---
name: site-design
description: Implementation guidance for establishing the visual foundation of a Liferay demo using Stylebooks and global CSS Client Extensions.
---

# Skill: Liferay Site Design (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for establishing the visual foundation of a Liferay demo using Stylebooks and global CSS Client Extensions. It is designed to be executed by a sub-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build site design assets from memory. You MUST use the `read_file` tool to read the following reference documents BEFORE acting:

- **Site Design Spec**: Read the provided technical specification (e.g., `specs/site-design/stylebook.md`).
- **Token Mapping Guide**: Read **[TOKEN_MAPPING_GUIDE.md](references/TOKEN_MAPPING_GUIDE.md)** to obtain the logic for correctly identifying and mapping tokens.

## Supplemental Guidance

### 1. Intent Analysis & Token Mapping
- **Analyze the Spec:** Identify the reference websites, brand colors, and aesthetic goals.
- **Source Verification:** Use `web_fetch` to retrieve the latest [frontend-token-definition.json](https://github.com/liferay/liferay-portal/blob/master/modules/apps/frontend-theme/frontend-theme-classic/src/WEB-INF/frontend-token-definition.json).
- **MANDATE (Strategic Relevance):** Focus your overrides ONLY on UI components relevant to the demo's use case. You do NOT need to change elements that will not be used or that can remain in their default "Classic" state.
- **MANDATE (Interaction Integrity):** For any component you DO customize (e.g., a button), you MUST map its interaction states (hover, active, focus) to ensure a polished look.
- **MANDATE (Show Your Work):** Before writing any files, you MUST list the tokens you have identified and mapped to the brand assets. Wait for internal validation against the `TOKEN_MAPPING_GUIDE.md`.

### 2. Implementation: Stylebook Assets
- **Objective:** Generate the raw JSON files required for a Liferay Stylebook import.
- **File 1: `style-book.json`** (Use `templates/style-book.json`).
- **File 2: `frontend-tokens-values.json`** (Use `templates/frontend-tokens-values.json`)
  - **MANDATE:** Every `cssVariableMapping` MUST exactly match the `value` field in the source JSON.
- **Storage:** Create the files in the `liferay/stylebooks/{stylebook_name}/` directory. The Orchestrator will handle zipping and delivery.

### 3. Implementation: CSS Client Extension
- **Location:** `liferay/client-extensions/{extension-name}/`
- **Structure:** `client-extension.yaml` and `assets/index.css`.
- **`index.css`:**
  - **MANDATE:** Exclusively use the `var(--token-name)` variables defined in the official Classic theme source. NO hardcoded values.

## Validation Phase
- **Integrated Check:** Verify that ALL variables used in the CSS and the Stylebook JSON exist in the official token definition.
- **Relevance Check:** Confirm that all key UI components required for the demo narrative have been correctly branded.
- **MANDATE:** Any variable used that is NOT in the official definition is strictly forbidden.

## Available Resources
- Liferay Learn - Stylebooks: https://learn.liferay.com/w/dxp/sites/site-appearance/style-books
- Liferay Learn - CSS Client Extensions: https://learn.liferay.com/w/dxp/development/customizing-liferays-look-and-feel/using-a-css-client-extension
- Reference: Token Mapping Guide: `references/TOKEN_MAPPING_GUIDE.md`
- Lexicon/Clay Documentation: https://clayui.com/
- Stylebook Templates: `templates/`
- Packaging Script: `scripts/package-stylebook.py`
