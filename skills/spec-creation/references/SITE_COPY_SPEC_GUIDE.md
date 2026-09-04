# Specification Guide: Cloned Site Copies (`liferay/specs/site-copy/[scenario-name]/`)

This reference document defines the mandatory sections and visual schemas for authoring Cloned Site Copy specifications.

---

## Mandatory Markdown Structure

Every Site Copy specification file MUST implement the following sections:

### 1. Environment & Target Inputs
*   **Source Site URL to Clone:** [Specify the external URL of the site to be cloned, e.g. `https://prospect-domain.com`]
*   **Target Portal Site Name:** [Specify the friendly, human-readable Site name]
*   **Target Portal Site ERC:** [Define the specific DXP Site ERC where this replica is assembled]
*   **Target Asset Space Name:** [Specify the friendly, human-readable Space name]
*   **Target Asset Space ERC:** [Define the high-level Space ERC used for Object-based CMS]

### 2. Existing Global Asset Auditing
The spec MUST list all pre-existing reusable assets using a single unified markdown table. Each entry must define:
*  `Type`: [Asset class, e.g. stylebook, fragment, content-structure, content-item, file-media]
*  `Name`: [Display name]
*  `Workspace Path`: [Folder relative on-disk path for development]
*  `System Location`: [The Space, Site, or Design Library container, including any hierarchical folders or fragment set paths]
*  `System ERC`: [The External Reference Code inside Liferay]

#### Mandatory Tabular Structure:
```
| Type | Name | Workspace Path | System Location (Container -> Path/Set) | System ERC |
| :--- | :--- | :--- | :--- | :--- |
| `[type]` | [Name] | [relative_path] | [Space/Site/Library -> Folder/Set] | [ERC] |
```
