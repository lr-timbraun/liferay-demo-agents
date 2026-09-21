# Specification Guide: Custom Elements (`liferay/specs/client-extensions/`)

This reference document defines the mandatory sections and project schemas for authoring React Custom Element specifications.

---

## Mandatory Markdown Structure

Every React Custom Element specification file MUST implement the following sections:

### 1. React SPA Structure
*  **Main Component Name:** Define the parent React component name, e.g. `MetricDashboard`.
*  **State Hooks:** Define state and effect variables required to drive the UI, e.g. useState, useEffect.
*  **Active Lifecycle Cleanups:** Enforce strict React 18 createRoot rendering and disconnectedCallback unmount handlers inside the custom element wrapper class to prevent memory leaks in the portal.

### 2. Client-Extension YAML Properties
Specify the variables mapped to the client extension descriptor:
*  `name`: Extension display name.
*  `type`: The standard Client Extension type, which must always be `customElement`.
*  `friendlyURL`: The static, friendly URL slug where the component resides.
*  `htmlId`: The HTML custom element selector tag registered in the DOM.
*  `urls`: Relative paths to compiled main bundle JS files on-disk.
