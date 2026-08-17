---
name: page-creation
description: Implementation guidance for programmatically creating Liferay Master Pages, Content Page Templates, and regular Content Pages inside a Site.
---

# Skill: Liferay Page Creation and Page Templates (Sub-Agent Implementation)

## Description
This skill provides implementation guidance and standard UI selectors for programmatically or interactively creating Liferay Master Pages, Content Page Templates, and regular Content Pages inside a Site. It is designed to be executed by sub-agents (such as the site-design-agent) to assemble beautiful site layouts.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build Liferay pages or configure templates from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating any automated browser scripts:

- **Page & Template Creation Guide**: You MUST read **[LIFERAY_PAGE_CREATION_GUIDE.md](references/LIFERAY_PAGE_CREATION_GUIDE.md)** to obtain the verified layout portlet URLs, Playwright browser-interaction selectors, drag-and-drop selectors, and publish commands.

## Supplemental Guidance

### 1. In-Browser Verification
- **Headed/Headless Execution:** Run browser interactions strictly using the `browser-use` skill (operating headlessly in the background to ensure reliable execution).
- **Screenshot Audits:** Capture screenshots during different phases (creation, fragment drag-and-drop, post-publication) to verify the visual layout and document successful rendering.

### 2. Page Hierarchy & Scopes
- **Master Pages First:** Always ensure your target Master Page is created and published before creating regular Content Pages, as those pages will inherit the Master Page's global headers and footers.
- **Content Page Templates:** When building repeatable layouts (like standard product detail templates or article detail layouts), package them inside a clean Page Template Collection/Set for easy reuse by content editors.

## Available Resources
- Liferay Learn - Master Pages: https://learn.liferay.com/w/dxp/site-building/developer-guide/layouts/master-pages
- Liferay Learn - Page Templates: https://learn.liferay.com/w/dxp/site-building/developer-guide/layouts/page-templates
- Reference: Liferay Page Creation and Page Templates Guide: `references/LIFERAY_PAGE_CREATION_GUIDE.md`
