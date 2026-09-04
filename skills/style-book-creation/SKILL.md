---
name: style-book-creation
description: Schema definition and variable mapping for Stylebook JSON files in Liferay DXP.
---

# Skill: Stylebook Creation (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for mapping corporate brand guidelines and color palettes into standard Liferay Stylebook import JSON payloads.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to map Stylebook variables from memory. You MUST read this skill description and the associated references BEFORE generating any Stylebook files:

- **Token Mapping Guide**: Read **[references/TOKEN_MAPPING_GUIDE.md](references/TOKEN_MAPPING_GUIDE.md)** to obtain the exact logic for identifying and mapping semantic brand variables.

## Supplemental Guidance

### 1. Token Source Verification
- Always map brand colors dynamically.
- Refer directly to Liferay's Classic theme token schema ([frontend-token-definition.json](https://github.com/liferay/liferay-portal/blob/master/modules/apps/frontend-theme/frontend-theme-classic/src/WEB-INF/frontend-token-definition.json)) to verify valid token names.

### 2. Implementation: Stylebook Assets
- **Location:** Place your Stylebook files under the `liferay/stylebooks/{stylebook_name}/` directory in the workspace.
- **Required Files:**
  1.  `style-book.json`: Defines the Stylebook name and base theme WAR ID (e.g. `classic_WAR_classictheme`).
  2.  `frontend-tokens-values.json`: Defines the actual variable values mapped to Liferay's standard Classic theme variable tokens.

## Available Resources
- Liferay Learn - Stylebooks: https://learn.liferay.com/w/dxp/sites/site-appearance/style-books
- Stylebook Schema Template: `templates/style-book.json`
- Token Values Template: `templates/frontend-tokens-values.json`
- Reference: Token Mapping Guide: `references/TOKEN_MAPPING_GUIDE.md`
