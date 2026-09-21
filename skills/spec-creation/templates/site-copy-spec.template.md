---
id: SPEC-[UNIQUE_UUID_OR_TASK_ID]
title: [Title]
type: site-copy
status: Planned
last_updated: YYYY-MM-DDTHH:MM:SSZ
---

# Specification: [Scenario Name]

## 1. Environment & Target Inputs
*   **Source Site URL to Clone:** [URL]
*   **Target Portal Instance Host:** [Host]
*   **Target Portal Site Name:** [Site Name]
*   **Target Portal Site ERC:** [Site ERC]
*   **Target Asset Space Name (Spaces):** [Space Name]
*   **Target Asset Space ERC (Spaces):** [Space ERC]

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
