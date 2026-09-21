# Specification Guide: Liferay Objects (`liferay/specs/objects/[object-name]/`)

This reference document defines the mandatory sections and schema schemas for authoring Custom Object specifications.

---

## Mandatory Markdown Structure

Every Object specification file MUST implement the following sections:

### 1. Definition Scope
*  **System Key:** `C_[ObjectName]` (Must contain capital C_ prefix, e.g. `C_SupportTicket`)
*  **Plural Name:** `C_[ObjectName]s`
*  **Scope:** [Specify whether the object resides globally or is scoped to a specific business Organization/Account]

### 2. Attribute Field Registry
Define the data fields of the Object:
*  `[fieldName]`: [Type: "string", "integer", "boolean", "date" | Required: true/false | Label]

### 3. Relationship Maps
Define connections to other Objects or standard portal entities:
*  `r_{relationshipName}_{relatedObject}Id`: [Type: "1:N" or "M:N" | Target Object Key]
