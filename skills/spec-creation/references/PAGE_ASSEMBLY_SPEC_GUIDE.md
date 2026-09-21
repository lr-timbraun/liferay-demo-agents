# Specification Guide: Page Assembly (`liferay/specs/pages/`)

This reference document defines the mandatory sections and layout schemas for authoring Master Templates and Content Page assembly specifications.

---

## Mandatory Markdown Structure

Every Page Assembly specification file MUST implement the following sections:

### 1. Environment & Target Inputs
*   **Target Portal Site Name:** Friendly, human-readable name of the destination site.
*   **Target Portal Site ERC:** Stable, persistent External Reference Code of the destination site.
*   **Target Design Library ERC:** Stable, persistent External Reference Code of the shared Design Library.
*   **Connected Space ERC:** Stable, persistent External Reference Code of the CMS Asset Space Library.

### 2. Master Page Template Layout
*   Define the Master Page Name, stable ERC, and the exact names/sets of the Global Header and Global Footer fragments to pin, creating the global visual shell of the copy.

### 3. Content Pages Hierarchy & Sequences
*   Provide a structured markdown table mapping out every target Content Page slug, page title, and the exact ordered sequence of Page Fragments to stack sequentially inside the Master Page's central Body Drop Zone.

### 4. Dynamic B2B Collections Wiring
*   Provide a structured markdown table detailing which repeating sliders, grids, or carousels must be connected to Liferay standard Collection Display widgets and dynamic Objects/Spaces data sources.
