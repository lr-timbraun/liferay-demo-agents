# Specification Guide: Page Fragments (`liferay/specs/fragments/`)

This reference document defines the mandatory sections and layout schemas for authoring Page Fragment specifications.

---

## Mandatory Markdown Structure

Every Fragment specification file MUST implement the following sections:

### 1. Visual Layout & HTML Structure
*  **Grid layout:** Define the visual grid container, flex scopes, and columns alignment.
*  **Typography:** Enforce CSS font sizes, headings, colors, and line heights.
*  **Structural HTML:** Specify mandatory HTML skeleton tags, container wrapping, and class names.

### 2. Configuration Options (`configuration.json`)
*  **Fields Registry:** Define options (colors, select dropdowns, text inputs) that the page editor displays:
  *  `fieldName`: Internal key of the option field.
  *  `type`: The standard configuration variable type, such as color, select, or text.
  *  `defaultValue`: Standard fallback value when none is selected.

### 3. Dynamic FreeMarker Variables (`restClient`)
*  **API Path:** Define the exact DXP REST endpoint to query, such as `/o/c/supporttickets`.
*  **looseDeserialize Map:** Enforce standard looseDeserialize keys to parse the JSON string response inside the FreeMarker script.
