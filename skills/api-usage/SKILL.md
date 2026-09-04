---
name: api-usage
description: Guidelines for calling Liferay REST APIs from client-side React code (Liferay.Util.fetch) or FreeMarker templates (restClient).
---

# Skill: API Usage (Headless Integration)

## Description
This skill provides authentication details, standard headers, and request schemas for executing dynamic reads/writes against Liferay DXP Headless REST endpoints.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to execute DXP REST fetches from memory. You MUST load and read these files BEFORE executing API usage tasks:
- **API Usage Guide**: Read **[references/API_USAGE_GUIDE.md](references/API_USAGE_GUIDE.md)** to obtain the exact headers and endpoint URL paths.

## Available Resources
- API Usage Guide: `references/API_USAGE_GUIDE.md`
