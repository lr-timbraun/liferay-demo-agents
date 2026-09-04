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

## Available Resources
- Liferay CSS Client Extension Guide: `references/LIFERAY_CSS_CLIENT_EXTENSION_GUIDE.md`
- Descriptor Template: `templates/client-extension.yaml`
- Stylesheet Template: `templates/custom.css`
