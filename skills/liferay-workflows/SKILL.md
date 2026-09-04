---
name: liferay-workflows
description: Guidelines for modeling multi-stage enterprise-grade Kaleo XML workflows in Liferay DXP.
---

# Skill: Liferay Workflows (Kaleo XML Modeling)

## Description
This skill provides schema details and guidelines for designing standard-compliant, multi-stage approval workflow processes using Liferay DXP's Kaleo XML engine.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to draft workflows from memory. You MUST load and read these files BEFORE executing workflow tasks:
- **Kaleo XML Reference Guide**: Read **[references/KALEO_XML_REFERENCE.md](references/KALEO_XML_REFERENCE.md)** to obtain the correct XML nodes, states, and action hooks schemas.

## Supplemental Guidance

### 1. Standard Transitions
- Every workflow task node MUST define an approval path transitioning to `approved` state, and a rejection path transitioning to `rejected` state.

## Available Resources
- Standard Workflow Template: `templates/standard-approval.xml`
