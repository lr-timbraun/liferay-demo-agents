---
name: global-js-creation
description: Structure, scripting rules, and deployment descriptors for global JS Client Extensions.
---

# Skill: Global JS Creation (Scripting overloads)

## Description
This skill provides guidelines and YAML schemas for configuring global Javascript overloads inside Liferay Workspace client extension descriptors.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to configure scripting descriptors from memory. You MUST load and read these files BEFORE executing global JS creation tasks:
- **Liferay JS Client Extension Guide**: Read **[references/LIFERAY_JS_CLIENT_EXTENSION_GUIDE.md](references/LIFERAY_JS_CLIENT_EXTENSION_GUIDE.md)** to obtain the exact YAML properties.

## Supplemental Guidance

### 1. File Location
- Place your Javascript files under the `liferay/client-extensions/{extension_name}/` directory.
- Ensure the folder contains a valid `client-extension.yaml` file defining the extension metadata.

## Validation & Linting
Before completing any JS Client Extension task, you MUST run the JS linter on your generated directory to verify YAML descriptors, parentheses balance, and DOMContentLoaded best practices:

```bash
python skills/global-js-creation/scripts/lint_js.py liferay/client-extensions/{extension_name}
```

## Available Resources
- Liferay JS Client Extension Guide: `references/LIFERAY_JS_CLIENT_EXTENSION_GUIDE.md`
- Descriptor Template: `templates/client-extension.yaml`
- Script Template: `templates/custom.js`
- Code Linter: `scripts/lint_js.py`
