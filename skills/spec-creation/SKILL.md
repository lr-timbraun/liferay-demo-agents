---
name: spec-creation
description: Standardizing Markdown specs schemas and templates for Fragments, Objects, Custom Elements, and Workflows.
---

# Skill: Specification Creation (Sub-Agent Implementation)

## Description
This skill provides the unified specification structures, templates, and formatting standards utilized by spec-authoring agents (Conductor and Site Copy Agent) to draft technical, zero-guesswork specifications inside `liferay/specs/`.

---

## General Specification Policy (Shared Mandates)

Every specification file created under `liferay/specs/` MUST adhere to the following shared standards:

### 1. Mandatory Unified Front Matter Header
Every spec file MUST start with this exact Front Matter header containing a unique tracking ID, status variable, and full ISO 8601 timestamp:
```
---
id: SPEC-[UNIQUE_UUID_OR_TASK_ID]
title: [Descriptive Specification Title]
type: [fragment | object | custom-element | site-copy | workflow]
status: [Planned | Drafted | User-Approved | Completed]
last_updated: YYYY-MM-DDTHH:MM:SSZ
---
```

### 2. Strict Read-on-Demand Protocol (Anti-Context-Bloat)
To preserve context window efficiency and prevent cognitive token bloat during spec authoring, you MUST NOT load multiple standards guides. You MUST adhere to this strict loading sequence:
1.  Read this `SKILL.md` file first to register the general metadata rules and tracking headers.
2.  Identify the exact type of asset specification you are preparing to author.
3.  Use your native `read_file` tool to load **ONLY the single, specific reference guide** matching that type from the `references/` directory.
4.  **You are strictly forbidden from reading any other reference guides** in the `references/` folder during that turn.

### 3. Mandatory Footer Sections (Additional Instructions & Changelog History)
Every specification file created under `liferay/specs/` MUST terminate with these exact two standard H2 sections:
*   **`## Additional Instructions`**: A dedicated section for capturing any special edge-case requirements, visual rules, or custom boundary guidelines.
*   **`## History`**: A standard Markdown changelog table tracking the file's incremental updates:
    ```
    ## History
    | Revision | Date | Author | Description of Changes |
    | :--- | :--- | :--- | :--- |
    | **v1.0** | YYYY-MM-DDTHH:MM:SSZ | Conductor | Initial specification draft |
    ```

---

## Type-Specific Skill Directories

| Spec Type | Target Directory | Active Reference Guide (Read on Demand ONLY) |
| :--- | :--- | :--- |
| **Page Fragment** | `liferay/specs/fragments/[collection-name]/fragments/[fragment-name]/` | **`references/FRAGMENT_SPEC_GUIDE.md`** |
| **Object Schema** | `liferay/specs/objects/[object-name]/` | **`references/OBJECT_SPEC_GUIDE.md`** |
| **Custom Element** | `liferay/specs/client-extensions/[extension-name]/` | **`references/CUSTOM_ELEMENT_SPEC_GUIDE.md`** |
| **Workflow Schema**| `liferay/specs/workflows/[workflow-name]/` | (Standard XML template) |
| **Site Copy Scenario** | `liferay/specs/site-copy/[scenario-name]/` | **`references/SITE_COPY_SPEC_GUIDE.md`** |

---

## Available Resources
- Fragment Template: `templates/fragment-spec.template.md`
- Object Template: `templates/object-spec.template.md`
- Custom Element Template: `templates/custom-element-spec.template.md`
- Site Copy Template: `templates/site-copy-spec.template.md`
- Workflow Template: `templates/workflow-spec.template.md`
