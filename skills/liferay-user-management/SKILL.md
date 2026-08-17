---
name: liferay-user-management
description: Implementation guidance for programmatically onboarding B2B business accounts, building organization hierarchies, defining postal addresses, provisioning user accounts, and mapping scoped roles.
---

# Skill: Liferay User and Account Management (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for programmatically onboarding B2B business accounts, creating multi-level organization hierarchies, defining billing and shipping postal addresses, linking users, and setting up complex, scoped roles. It is designed to be executed by the user-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build Liferay user directories, accounts, or organizations from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating any Python data-population scripts:

- **User & Account Onboarding Guide**: Read **[USER_ACCOUNT_ONBOARDING_GUIDE.md](references/USER_ACCOUNT_ONBOARDING_GUIDE.md)** to obtain the verified REST API endpoints, parent-child organization JSON payloads, strict country/region postal address rules, and React-scoped role flattener boilerplates.

## Supplemental Guidance

### 1. Spec Ingestion
- **Read the Spec:** Locate and read the provided technical specification (e.g., specs/objects/user-onboarding.md).
- **Analyze Intent:** Identify the required accounts, geographic organization locations, postal addresses, and the specific user role briefs needed.

### 2. Implementation: Project Structure & Credentials
- **Location:** Place any generated Python populator scripts inside the assigned directory relative to the workspace root (e.g. `scripts/onboard-users.py`).
- **Credentials:** You MUST NOT read or parse the local `.env` file directly. You MUST import and use the `env_utils` script (`get_host()`, `get_admin_email()`, `get_admin_password()`) to securely resolve credentials and host URLs for all scripts.

### 3. Country and Region Guard
- **Strict Validation:** Liferay requires country and region names to match its built-in dictionary exactly (e.g. `"United Kingdom"` and `"London, City of"`).
- **Mishap Protection:** You MUST wrap your postal address API creation blocks inside a Python `try/catch` block to gracefully log region-matching failures rather than letting the script crash, ensuring the rest of the onboarding run succeeds.

## Available Resources
- Liferay Learn - Accounts: https://learn.liferay.com/w/dxp/building-applications/core-framework/accounts
- Liferay Learn - Organizations: https://learn.liferay.com/w/dxp/users-and-permissions/organizations
- Reference: User, B2B Account, and Organization Onboarding Guide: `references/USER_ACCOUNT_ONBOARDING_GUIDE.md`
