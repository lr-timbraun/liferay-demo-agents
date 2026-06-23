# Reference: Liferay Object Definition Schema

This document provides the mandatory field requirements and schema logic for constructing Liferay Object Definition payloads. Use this as a reference when preparing the JSON payload for the `create-object-definition.py` script.

## Required Root Properties
- **`name`**: The internal system name (CamelCase, e.g., `SupportTicket`).
- **`label`**: A dictionary containing the display name: `{"en_US": "Support Ticket"}`.
- **`pluralLabel`**: A dictionary for the plural display name.
- **`scope`**: MUST be set to `company` for global demo availability.
- **`active`**: MUST be `true`.
- **`externalReferenceCode`**: MUST be a unique UUID to ensure demo portability.
- **`panelCategoryKey`**: Set to `control_panel.users` to make it visible in the Liferay menu.

## Object Field Requirements
Every field in the `objectFields` array must define the following:
- **`name`**: internal name (e.g., `ticketStatus`).
- **`label`**: localized display name.
- **`DBType`**: The database storage type.
- **`businessType`**: The UI presentation type.
- **`indexed`**: Set to `true` ONLY if it makes sense for the field to be searchable or filterable. For internal IDs or large HTML content that does not need to be indexed, set to `false`.
- **`required`**: As defined in the Orchestrator's spec.

## Field Type Mapping Reference
| Field Goal | DBType | businessType |
| :--- | :--- | :--- |
| Short Text | `String` | `Text` |
| Long Text / HTML | `String` | `LongText` |
| Whole Number | `Integer` | `Integer` |
| Decimal | `BigDecimal` | `Decimal` |
| Date Only | `Date` | `Date` |
| Date & Time | `DateTime` | `DateTime` |
| True/False | `Boolean` | `Boolean` |
| Attachment | `Long` | `Attachment` |

## Defining Relationships
Liferay Objects support connections to other entities via the `objectRelationships` array in the root payload.

### Core Properties:
- **`name`**: The internal name of the relationship (e.g., `ticketsToUsers`).
- **`type`**: `oneToMany` or `manyToMany`.
- **`deletionType`**: Use `cascade` to ensure demo data remains clean when parents are deleted.
- **`objectDefinitionExternalReferenceCode2`**: The ERC of the target Object (or System entity).

### Usage in Entries:
To link an entry during population, the sub-agent MUST use the following naming convention for the relationship field:
`r_{relationshipName}_{relatedObject}Id` (e.g., `r_ticketsToUsers_userId`).

## Implementation Workflow
1.  Analyze the Orchestrator's spec for the required schema.
2.  Construct a JSON payload following this schema and the `templates/object-definition.json` structure.
3.  Execute the payload using: `python scripts/create-object-definition.py <path_to_json>`
