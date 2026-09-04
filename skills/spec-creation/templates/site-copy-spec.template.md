---
id: SPEC-[UNIQUE_UUID_OR_TASK_ID]
title: [Descriptive Specification Title]
type: site-copy
status: Planned
last_updated: YYYY-MM-DDTHH:MM:SSZ
---

# Specification: [Scenario Name]

## 1. Environment & Target Inputs
*   **Source Site URL to Clone:** [Specify the external URL of the site to be cloned, e.g. https://yarefil-manufacturing.com]
*   **Target Portal Instance Host:** [e.g., https://localhost]
*   **Target Portal Site Name:** [Specify the friendly, human-readable Site name, e.g. Yarefil Cardiovascular Storefront]
*   **Target Portal Site ERC:** [Define the specific DXP Site External Reference Code where this replica must be assembled]
*   **Target Asset Space Name (Spaces):** [Specify the friendly, human-readable Space name, e.g. Yarefil Cardio Assets Space]
*   **Target Asset Space ERC (Spaces):** [Define the high-level Space ERC used for Object-based CMS and Media]

## 2. Existing Global Asset Auditing
| Type | Name | Workspace Path | System Location (Container -> Path/Set) | System ERC |
| :--- | :--- | :--- | :--- | :--- |
| `stylebook` | Acme Stylebook | `liferay/stylebooks/my-stylebook/` | `Design Library -> Stylebooks` | `yarefil-stylebook-erc` |
| `global-css` | Theme Overrides | `liferay/client-extensions/my-css/` | `Client Extensions -> globalCSS` | `yarefil-css-erc` |
| `page-master` | Home Page Master | `liferay/pages/master/` | `Acme Site -> Page Templates -> Masters` | `master-page-erc` |
| `fragment` | Product Card | `liferay/fragments/my-set/my-card/` | `Design Library -> Fragment Sets -> My Set` | `fragment-my-card-erc` |
| `content-structure`| News Article | `liferay/content/structures/` | `My Space -> Web Content Structures` | `C_NewsArticleStructure` |
| `content-item` | Press Release | `liferay/content/items/` | `My Space -> Web Content -> Press Releases/` | `article-press-release-erc` |
| `file-media` | Hero Background | `liferay/content/files/` | `My Space -> Documents -> Banner_Images/` | `file-hero-background-erc` |

## Additional Instructions

## History
| Revision | Date | Author | Description of Changes |
| :--- | :--- | :--- | :--- |
| **v1.0** | YYYY-MM-DDTHH:MM:SSZ | Conductor | Initial specification draft |
