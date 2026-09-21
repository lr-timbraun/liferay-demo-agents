# Specification Guide: Page Assembly (`liferay/specs/pages/`)

This reference document defines the mandatory sections and layout schemas for authoring Master Templates and Content Page assembly specifications.

---

## Mandatory Markdown Structure

Every Page Assembly specification file MUST implement the following sections:

### 1. Environment & Target Inputs
*   **Target Portal Site Name:** [Friendly Site name]
*   **Target Portal Site ERC:** [Stable ERC of the destination site]
*   **Target Design Library ERC:** [Stable ERC of the Design Library]
*   **Connected Space ERC:** [Stable ERC of the CMS Asset Space Library]

### 2. Master Page Template Layout
*   [Specify Master Page Name, stable ERC, and the exact names/sets of the Global Header and Global Footer fragments to pin]

### 3. Content Pages Hierarchy & Sequences
*   [Provide a structured markdown table mapping out every target Content Page slug, page title, and the exact ordered sequence of Page Fragments to stack inside the drop zone]

### 4. Dynamic B2B Collections Wiring
*   [Provide a structured markdown table detailing which repeating sliders or grids must be connected to Liferay standard Collection Display widgets and dynamic Objects/Spaces data sources]
