---
name: create-custom-element
description: Implementation guidance for creating React-based Custom Element Client Extensions in Liferay.
---

# Skill: Create Custom Element (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for creating sophisticated, decoupled UI components using React-based Custom Element Client Extensions. It is designed to be executed by a sub-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build React-based client extensions from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating any code:

- **React CX Guide**: Read **[REACT_CUSTOM_ELEMENT_GUIDE.md](references/REACT_CUSTOM_ELEMENT_GUIDE.md)** to obtain the verified project structure, `client-extension.yaml` configuration, and React mounting logic.

## Supplemental Guidance

### 1. Spec Ingestion
- **Read the Spec:** Locate and read the provided technical specification (e.g., `specs/client-extensions/user-dashboard.md`).
- **Identify Technology:** Unless otherwise specified, you MUST use **React** for all custom element development.

### 2. Implementation: Project Structure
- **Location:** `liferay/client-extensions/{project-name}/`
- **Mandatory Logic:**
  - Every project must include a valid `client-extension.yaml` with an `assemble` block.
  - React components MUST be mounted within a standard Web Component class using `createRoot`.
  - Use `/* global Liferay */` for all platform API interactions.

### 3. Styling & Polish
- **MANDATE:** You MUST exclusively use `var(--token-name)` for all declarations where a matching Classic theme token exists.
- **Isolation:** Ensure React component styling is scoped to prevent collisions with the theme.

### 4. Validation Phase
- **Build Simulation:** Verify that the `assemble` block correctly maps `build/static` to `static`.
- **YAML Validation:** Ensure `htmlElementName` matches the custom element definition in the JS source.
- **Interaction Check:** Confirm `disconnectedCallback` correctly unmounts the React root to prevent memory leaks.

## Available Resources
- Liferay Learn - Using a Custom Element Client Extension: https://learn.liferay.com/w/dxp/development/customizing-liferays-look-and-feel/using-a-custom-element-client-extension
- Lexicon/Clay Documentation: https://clayui.com/
- Reference: React Custom Element Guide: `references/REACT_CUSTOM_ELEMENT_GUIDE.md`
- **Official Liferay Custom Element Samples:**
  - [Sample 1](https://github.com/liferay/liferay-portal/tree/master/workspaces/liferay-sample-workspace/client-extensions/liferay-sample-custom-element-1)
  - [Sample 2](https://github.com/liferay/liferay-portal/tree/master/workspaces/liferay-sample-workspace/client-extensions/liferay-sample-custom-element-2)
  - [Sample 3](https://github.com/liferay/liferay-portal/tree/master/workspaces/liferay-sample-workspace/client-extensions/liferay-sample-custom-element-3)
