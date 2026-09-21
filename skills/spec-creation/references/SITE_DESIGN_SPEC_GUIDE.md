# Specification Guide: Site Design (`liferay/specs/site-design/`)

This reference document defines the mandatory sections and visual schemas for authoring Site Design (Styling Brief) specifications.

---

## Mandatory Markdown Structure

Every Site Design specification file MUST implement the following sections:

### 1. Environment, Sources & Target Inputs
*   **Target Portal Site Name:** Friendly, human-readable name of the destination site.
*   **Target Portal Site ERC:** Stable, persistent External Reference Code of the destination site.
*   **Target Design Library ERC:** Stable, persistent External Reference Code of the shared Design Library.
*   **Sourced Branding Assets Workspace Reference:** The relative path inside the local liferay/input/ directory where the original crawled logo, stylesheets, and style guides are stored.

### 2. Extracted Original Brand Assets (Tabular Schema)
The specification must list all pre-existing crawled assets using a single unified markdown table. Each entry must define:
*   `Asset Name`: The specific asset or property name crawled, such as Primary Brand Color, Logo Path, or Background SVG.
*   `Extracted Value`: The exact, crawled value, such as #0056B3 or liferay/input/logo.png.
*   `Description`: Detailed textual description of where the asset was located or its visual role, for human readers.
*   **CRITICAL BOUNDARY RULE:** The spec-authoring agent is strictly forbidden from injecting, inventing, or designing any custom styles, colors, or visual overloads into this original brand assets list. This section must strictly and exclusively contain only the literal, unmodified assets and parameters physically extracted from the original crawled site.

### 3. Brand Identity & Design Brief (Aesthetic & User Personas)
*   **Aesthetic & Archetype Brief:** Provide a verbose, descriptive brief of the target visual brand design. This area has less enforced structure, allowing for a detailed narrative describing the overall styling directions, theme feel, archetype styling guidelines, color mood, and typographical goals.
*   **User Personas:** Outline and define all the different users and personas of the platform who will interact with this site layout (such as B2B buyers, administrative users, field operators, or support staff), detailing their respective roles and user-experience expectations.
