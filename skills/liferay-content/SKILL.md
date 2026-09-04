---
name: liferay-content
description: Modeling Liferay Web Content Structures (JSON) and FreeMarker templates, managing documents, files, and assets inside modern Spaces.
---

# Skill: Liferay Content (Structured CMS)

## Description
This skill provides guidelines and templates for modeling structured B2B content schemas (JSON Structures) and dynamic FreeMarker templates inside modern DXP Spaces.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write content structures or FreeMarker scripts from memory. You MUST load and read these files BEFORE executing content creation tasks:
- **Liferay Content Structure Guide**: Read **[references/LIFERAY_CONTENT_STRUCTURE_GUIDE.md](references/LIFERAY_CONTENT_STRUCTURE_GUIDE.md)** to obtain the exact JSON schema formats.
- **Liferay Content Template Guide**: Read **[references/LIFERAY_CONTENT_TEMPLATE_GUIDE.md](references/LIFERAY_CONTENT_TEMPLATE_GUIDE.md)** to obtain the standard FreeMarker display helpers.

## Supplemental Guidance

### 1. Modern DXP Spaces
- Do not target legacy, classic Sites for content storage. Always structured and map assets inside global Design Libraries or modern **Spaces** to ensure separation of concerns.

## Available Resources
- Content Structure Template: `templates/content-structure.json`
- Content Template Template: `templates/content-template.ftl`
