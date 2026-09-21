---
name: global-css-creation
description: Structure, styling rules, and deployment descriptors for global CSS Client Extensions.
---

# Skill: Global CSS Creation (Styling overrides)

## Description
This skill provides guidelines and YAML schemas for configuring global CSS overrides inside Liferay Workspace client extension descriptors.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to configure stylesheet descriptors from memory. You MUST load and read these files BEFORE executing global CSS creation tasks:
- **Liferay CSS Client Extension Guide**: Read **[references/LIFERAY_CSS_CLIENT_EXTENSION_GUIDE.md](references/LIFERAY_CSS_CLIENT_EXTENSION_GUIDE.md)** to obtain the exact YAML properties.

## Supplemental Guidance

### 1. File Location
- Place your CSS files under the `liferay/client-extensions/{extension_name}/` directory.
- Ensure the folder contains a valid `client-extension.yaml` file defining the extension metadata.

### 2. CSS Namespacing & Administrative Scope Protection
- **CRITICAL SCOPING RULE:** To prevent custom styling rules from leaking into and breaking Liferay's administrative overlays, control panels, editing frames, or page-editor sidebars, you MUST NOT write raw global element selectors (like `body`, `button`, `a`, `div`, `.btn`, `.form-control`) inside your global `custom.css`.
- **Strict Scoping:** All custom global CSS selectors MUST be strictly namespaced under a site-specific parent class or a unique container wrapper (for example, wrapping overrides inside site-specific body classes or unique layout containers like `.site-name-wrapper .btn`). This guarantees that Liferay's parent workspace and administrative controls remain fully isolated and completely unaffected.

## Validation & Linting
Before completing any CSS Client Extension task, you MUST run the CSS linter on your generated directory to verify YAML descriptors and balanced curly-braces syntax:

```bash
python skills/global-css-creation/scripts/lint_css.py liferay/client-extensions/{extension_name}
```

## Available Resources
- Liferay CSS Client Extension Guide: `references/LIFERAY_CSS_CLIENT_EXTENSION_GUIDE.md`
- Descriptor Template: `templates/client-extension.yaml`
- Stylesheet Template: `templates/custom.css`
- Code Linter: `scripts/lint_css.py`
