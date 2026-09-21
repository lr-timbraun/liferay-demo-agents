# Specification Guide: Custom Elements (`liferay/specs/client-extensions/[extension-name]/`)

This reference document defines the mandatory sections and project schemas for authoring React Custom Element specifications.

---

## Mandatory Markdown Structure

Every React Custom Element specification file MUST implement the following sections:

### 1. React SPA Structure
*  **Main Component Name:** [e.g. "MetricDashboard"]
*  **State Hooks:** [Define state and effect variables, e.g. useState, useEffect]
*  **Active Lifecycle Cleanups:** [Enforce strict React 18 createRoot rendering and disconnectedCallback unmount handlers to prevent memory leaks]

### 2. Client-Extension YAML Properties
Specify the variables mapped to the client extension descriptor:
*  `name`: [Extension display name]
*  `type`: `customElement`
*  `friendlyURL`: `/[extension-url-slug]`
*  `htmlId`: `[html-custom-element-selector]`
*  `urls`: [e.g. js/main.*.js]
