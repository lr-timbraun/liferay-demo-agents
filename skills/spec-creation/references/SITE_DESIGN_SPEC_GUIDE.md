# Specification Guide: Site Design (`liferay/specs/site-design/`)

This reference document defines the mandatory sections and visual schemas for authoring Stylebook and CSS/JS Client Extension specifications.

---

## Mandatory Markdown Structure

Every Site Design specification file MUST implement the following sections:

### 1. Environment & Target Inputs
*   **Target Portal Site Name:** [Friendly Site name]
*   **Target Portal Site ERC:** [Stable ERC of the destination site]
*   **Target Design Library ERC:** [Stable ERC of the shared Design Library]

### 2. Stylebook Configuration
*   [Define a clear delta variables mapping list for brand Colors, Typography, and Border-radius token variables]

### 3. Global CSS Client Extension
*   [Specify mandatory stylesheet filename, layout scoping, custom container overrides, and key visual 'wow' animation rules]

### 4. Global JS Client Extension
*   [Specify mandatory script filename, DOM-loaded selectors, custom UI triggers, and active scroll state handlers]
