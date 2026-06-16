---
name: liferay-objects
description: Implementation guidance for programmatically creating, publishing, and populating Liferay Objects.
---

# Skill: Liferay Objects (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for programmatically creating, publishing, and populating Liferay Objects. It is designed to be executed by a sub-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write Object creation or population scripts from memory. You MUST use the `read_file` tool to read the following reference documents BEFORE generating any code:

- **Object Definition**: Read **[OBJECT_DEFINITION_CREATION.md](references/OBJECT_DEFINITION_CREATION.md)** to obtain the validated field requirements and schema logic.
- **Object Population**: Read **[OBJECT_ENTRY_POPULATION.md](references/OBJECT_ENTRY_POPULATION.md)** to obtain the templates and industry-relevance standards for generating demo data entries.
- **API Payloads**: Read **[templates/object-definition.json](templates/object-definition.json)** to obtain the exact JSON structure required for Object Definition creation.

## Supplemental Guidance

### 1. Spec Ingestion
- **Read the Spec:** Locate and read the provided technical specification (e.g., `specs/objects/support-ticket.md`).
- **Analyze Schema:** Identify the field names, types, labels, and relationships defined by the Orchestrator.
- **Contract Compliance:** You MUST strictly adhere to the field names and data types specified in the spec to ensure interoperability with related Fragments.

### 2. Implementation Preparation
- **Credentials:** You MUST use the `LIFERAY_ADMIN_EMAIL_ADDRESS` and `LIFERAY_ADMIN_PASSWORD` from the local `.env` file for all API-driven scripts.
- **Python Setup:** Ensure the `requests` library is installed (`pip install requests`).

### 3. Implementation: API-Driven Workflow
- **Step 1: Definition:** Use the JSON structure in `templates/object-definition.json` to construct your payload.
  - Run the automated script: `python scripts/create-object-definition.py <path_to_payload.json>`
  - This script handles both the creation and publication of the Object.
- **Step 2: Population:** Use the pattern in `OBJECT_ENTRY_POPULATION.md` to generate and submit industry-specific demo data.

### 4. Interoperability & Relationships
- **Relationship Fields:** When linking to other entities, follow the `r_{relationshipName}_{relatedObject}Id` naming convention.
- **Data Consistency:** Ensure that the data you populate matches the field types expected by the corresponding UI Fragments.

### 5. Validation Phase
- **API Check:** Verify that the Object exists and is `published`.
- **Entry Check:** Perform a `GET` request to the Object's REST endpoint to confirm entries were successfully created.

## Available Resources
- Liferay Learn - Objects Overview: https://learn.liferay.com/w/dxp/building-applications/objects
- Liferay Learn - Headless Admin Objects API: https://learn.liferay.com/w/dxp/integration/headless-apis/object-apis/custom-object-apis
- Reference: Object Definition Guide: `references/OBJECT_DEFINITION_CREATION.md`
- Reference: Object Population Guide: `references/OBJECT_ENTRY_POPULATION.md`
- Template: Object Definition Payload: `templates/object-definition.json`
- Automation Script: `scripts/create-object-definition.py`
