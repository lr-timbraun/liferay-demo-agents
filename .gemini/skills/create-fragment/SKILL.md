---
name: create-fragment
description: Implementation guidance for creating high-impact Liferay UI Fragments, including standard and Form fragments.
---

# Skill: Create Fragment (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for creating high-impact Liferay UI Fragments, including standard and Form fragments. It is designed to be executed by a sub-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build fragments from memory. You MUST use the `read_file` tool to read the following reference documents BEFORE generating any code:

- **Fragment Development Guide**: Read **[FRAGMENT_REFERENCE_GUIDE.md](references/FRAGMENT_REFERENCE_GUIDE.md)** for best practices and common import error solutions.
- **Configuration Types**: Read **[FRAGMENT_LFR_CONFIGURATION_TYPES.md](references/FRAGMENT_LFR_CONFIGURATION_TYPES.md)** to verify valid field types for `configuration.json`.
- **Editable Types**: Read **[FRAGMENT_LFR_EDITABLE_TYPES.md](references/FRAGMENT_LFR_EDITABLE_TYPES.md)** to verify valid `lfr-editable` syntax for dynamic content.
- **Form Fragments**: Read **[FORM_FRAGMENT_DEVELOPMENT_GUIDE.md](references/FORM_FRAGMENT_DEVELOPMENT_GUIDE.md)** if building fragments for Form Containers.
- **API Calls (FreeMarker)**: Read **[FRAGMENT_API_CALLS_FREEMARKER.md](references/FRAGMENT_API_CALLS_FREEMARKER.md)** if the fragment needs to fetch data from Liferay Objects or Headless APIs using FreeMarker.

## Supplemental Guidance

### 1. Spec Ingestion
- **Read the Spec:** Locate and read the provided technical specification (e.g., `specs/fragments/hero-banner.md`).
- **Analyze Intent:** Identify the required HTML structure, visual style, and the types of content (text, image, etc.) that need to be dynamic.

### 2. Implementation: Fragment Structure
- **Root Location:** `liferay/fragments/{collection-name}/`
- **Collection Metadata:** Every collection folder MUST contain a `collection.json` file defining the set's name and description.
- **Fragments Subdirectory:** All individual fragments MUST be stored within a `fragments/` subfolder of the collection folder.
- **Mandatory Hierarchy Pattern:**
  ```text
  {collection-name}/
  ├── collection.json
  └── fragments/
      ├── {fragment-name}/
      │   ├── fragment.json      (Defines metadata and file paths)
      │   ├── configuration.json (MANDATORY: Defines configurable fields)
      │   ├── index.html         (MANDATORY: Markup - may be empty)
      │   ├── index.css          (MANDATORY: Styling - may be empty)
      │   └── index.js           (MANDATORY: Interactivity - may be empty)
  ```

### 3. Styling & Polish
- **MANDATE:** You MUST exclusively use `var(--token-name)` for all declarations where a matching Classic theme token exists.
- **Lexicon/Clay:** Use Clay CSS classes for consistent Liferay UI patterns.

### 4. Implementation: Dynamic Data & Forms
- **Liferay Objects:** For dynamic data, use the `lfr-editable` attribute instead of configuration mapping.
- **Form Fragments:** If building for a form, you MUST bind input attributes to the system-provided `${input}` variable.
- **Server-Side Data:** Use the `restClient` object for all server-side API calls within the fragment template.

### 5. Validation Phase
- **Structural Integrity:** Verify the fragment is in the correct `liferay/fragments/` directory and contains all mandatory files (including `configuration.json`).
- **File References:** Ensure `fragment.json` contains the correct `configurationPath: "configuration.json"` key.
- **Styling Check:** Ensure NO hardcoded colors or spacing exist in `index.css`.
- **Form Mapping:** For form fragments, confirm that `name="${input.name}"` is correctly implemented.

## Available Resources
- Liferay Learn - Developing Page Fragments: https://learn.liferay.com/w/dxp/development/developing-page-fragments
- Liferay Learn - Creating Form Fragments: https://learn.liferay.com/w/dxp/sites/creating-pages/page-fragments-and-widgets/using-fragments/using-form-fragments/creating-form-fragments
- Lexicon/Clay Documentation: https://clayui.com/
- Reference: Fragment Development Guide: `references/FRAGMENT_REFERENCE_GUIDE.md`
- Reference: Configuration Types: `references/FRAGMENT_LFR_CONFIGURATION_TYPES.md`
- Reference: Editable Types: `references/FRAGMENT_LFR_EDITABLE_TYPES.md`
- Reference: Form Fragment Guide: `references/FORM_FRAGMENT_DEVELOPMENT_GUIDE.md`
- Reference: API Calls (FreeMarker): `references/FRAGMENT_API_CALLS_FREEMARKER.md`
