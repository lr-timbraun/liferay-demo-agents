---
id: SPEC-[UNIQUE_UUID_OR_TASK_ID]
title: [Descriptive Specification Title]
type: page-assembly
status: Planned
last_updated: YYYY-MM-DDTHH:MM:SSZ
---

# Specification: [Page Assembly Name]

## 1. Environment & Target Inputs
*   **Target Portal Site Name:** [Specify friendly Site name, e.g. Everflow Utilities Storefront]
*   **Target Portal Site ERC:** [Define the target Site ERC, e.g. everflow-site-erc]
*   **Target Design Library ERC:** [Define the target Design Library ERC where Page Fragments reside]
*   **Connected Space ERC (Spaces):** [Define the Space ERC used for Object-based CMS and media]

## 2. Master Page Template Layout
*   **Master Page Name:** [Specify the name, e.g. Everflow Master Page]
*   **Master Page ERC:** [Specify the stable ERC, e.g. everflow-master-erc]
*   **Global Header Fragment:** [Specify the Header Fragment ERC and its parent Collection]
*   **Global Footer Fragment:** [Specify the Footer Fragment ERC and its parent Collection]

## 3. Content Pages Hierarchy & Sequences
The page body must be assembled by stacking the respective body Page Fragments sequentially inside the Master Page's central Body Drop Zone:

| Page URL / Slug | Page Title | Page Description | Fragments Stack Sequence (Ordered Top-to-Bottom) |
| :--- | :--- | :--- | :--- |
| `/home` | Home Page | Corporate storefront primary landing page | `1. everflow-set -> hero-card`<br>`2. everflow-set -> features-grid`<br>`3. everflow-set -> promo-card` |
| `/services` | Our Services | Industrial utility support and services catalog | `1. everflow-set -> services-hero`<br>`2. everflow-set -> services-grid` |

## 4. Dynamic B2B Collections Wiring
Repeating visual cards, list elements, or carousels must loop a single Fragment card dynamically over Space content or custom Object records using standard Liferay Collection Display widgets:

| Target Page / Zone | Repeating Component Description | Connected Collection Provider / Object Key |
| :--- | :--- | :--- |
| `/home` / Features Grid | 3-column components classifications repeat | Connected to standard Space category vocabulary folders |
| `/services` / Services Grid | Regional maintenance support catalog list | Connected to custom Object dataset `C_ServiceCatalog` |

---

## Additional Instructions

## History
| Revision | Date | Author | Description of Changes |
| :--- | :--- | :--- | :--- |
| **v1.0** | YYYY-MM-DDTHH:MM:SSZ | Conductor | Initial specification draft |
