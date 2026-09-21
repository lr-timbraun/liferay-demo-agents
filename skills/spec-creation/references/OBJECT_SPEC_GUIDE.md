# Specification Guide: Liferay Objects (`liferay/specs/objects/`)

This reference document defines the mandatory sections and schema schemas for authoring Custom Object specifications.

---

## Mandatory Markdown Structure

Every Object specification file MUST implement the following sections:

### 1. Definition Scope
*  **System Key:** Custom Object names must always contain the uppercase `C_` prefix to comply with Liferay Object standards, e.g. `C_SupportTicket`.
*  **Plural Name:** Custom plural name of the object definition, e.g. `C_SupportTickets`.
*  **Scope:** Specify whether the object resides globally (company scope) or is scoped to a specific business Organization or B2B Account directory.

### 2. Attribute Field Registry
Define the data fields of the Object:
*  `fieldName`: The database-safe key of the attribute field, including its variable data type (string, integer, boolean, date), required status, and user-facing label.

### 3. Relationship Maps
Define connections to other Objects or standard portal entities:
*  `r_relationshipName_relatedObjectId`: Define the relationship key, transition type (1:N or M:N), and target Object key.
