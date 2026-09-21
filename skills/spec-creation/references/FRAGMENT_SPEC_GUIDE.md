# Specification Guide: Page Fragments (`liferay/specs/fragments/`)

This reference document defines the mandatory sections and layout schemas for authoring Page Fragment specifications.

---

## Mandate: High Modularity & Granular Reusability (CRITICAL)

Custom Page Fragments MUST be designed and specified as highly modular, single components of a page layout (such as a Hero Banner, a specific Product Card, a Testimonial slider, a CTA Button, or a dynamic Feature block).
* **NO Full-Page Fragments:** You are strictly forbidden from specifying or building "full page fragments" or bundling an entire page layout (such as header, body features, forms, and footers) into a single monolithic fragment.
* **Proper Liferay Assembly:** A proper, high-quality Liferay page is constructed by dragging and dropping multiple small, reusable modular fragments onto the layout canvas. Do not attempt to short-circuit this by writing monolithic layouts.

---

## Mandatory Markdown Structure

Every Fragment specification file MUST implement the following sections:

### 1. Visual Layout & HTML Structure
*  **Grid layout:** [Define the visual grid container, flex scopes, and columns alignment]
*  **Typography:** [Enforce CSS font sizes, headings, colors, and line heights]
*  **Structural HTML:** [Specify mandatory HTML skeleton tags, container wrapping, and class names]

### 2. Configuration Options (`configuration.json`)
*  **Fields Registry:** Define options (colors, select dropdowns, text inputs) that the page editor displays:
  *  `fieldName`: [Internal key]
  *  `type`: [ListType type: e.g. "color", "select", "text"]
  *  `defaultValue`: [Standard fallback]

### 3. Dynamic FreeMarker Variables (`restClient`)
*  **API Path:** [Define the exact DXP REST endpoint to query, e.g. `/o/c/supporttickets`]
*  **looseDeserialize Map:** [Enforce standard looseDeserialize keys to parse the JSON string response]
