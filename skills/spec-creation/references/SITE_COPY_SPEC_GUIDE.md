# Specification Guide: Cloned Site Copies (`liferay/specs/site-copy/[scenario-name]/`)

This reference document defines the mandatory sections and visual schemas for authoring Cloned Site Copy specifications.

---

## Mandatory Markdown Structure

Every Site Copy specification file MUST implement the following sections:

### 1. Environment & Target Inputs
*   **Source Site URL to Clone:** The external URL of the site to be cloned, which the Site Copy Agent will use as its crawling target.
*   **Target Portal Site Name:** Friendly, human-readable name of the destination site.
*   **Target Portal Site ERC:** Stable, persistent External Reference Code of the destination site.
*   **Target Asset Space Name:** Friendly, human-readable name of the connected Space used for media and content.
*   **Target Asset Space ERC:** Stable, persistent External Reference Code of the connected Space.

### 2. Existing Global Asset Auditing
The specification must list all pre-existing reusable assets using a single unified markdown table to prevent duplicate asset creation on disk. Each entry must define:
*   `Type`: The asset class, such as stylebook, fragment, content-structure, content-item, or file-media.
*   `Name`: Friendly display name of the existing asset.
*   `Workspace Path`: The relative folder path inside the local workspace for development lookup.
*   `System Location`: The Space, Site, or Design Library container where the asset resides, including folder hierarchies.
*   `System ERC`: The stable External Reference Code of the asset inside the portal.

#### Mandatory Tabular Structure:
```
| Type | Name | Workspace Path | System Location (Container -> Path/Set) | System ERC |
| :--- | :--- | :--- | :--- | :--- |
| [type] | [Name] | [relative_path] | [Space/Site/Library -> Folder/Set] | [ERC] |
```
