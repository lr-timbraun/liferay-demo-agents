# Liferay Demo Agent Framework

This repository houses the configuration, specialized agent personas, custom skills, and local automation scripts designed for **Gemini CLI** (and other compatible AI tools) to automate the development, packaging, and validation of Liferay DXP demonstrations locally using **Liferay Docker Manager (LDM)** and **Blade CLI**.

It is tailored specifically for building visually stunning, "Boardroom Ready" proof-of-concepts and demos with speed, consistency, and structural integrity.

---

## 🚀 Key Features

*   **Orchestrator/Sub-Agent Workflow:** Separates strategic planning (Phase 1) from granular implementation (Phase 2) and final delivery/validation (Phase 3).
*   **Specialized Agent Personas:** Dedicated configurations for `site-design`, `fragment`, `object`, and `custom-element` development.
*   **Concurrently Isolated Execution:** Sub-agents are restricted to their assigned directories, enabling multiple agents to run in parallel without file collisions.
*   **Automated Deployment Scripts:** A suite of local Python scripts that automate compiling, packaging, and hot-deploying Stylebooks, Fragments, and Client Extensions.
*   **End-to-End Persona Validation:** Mandates the creation of a `liferay/specs/TEST_PLAN.md` which performs visual, interactive, in-session browser testing on the live site.

---

## 🛠️ Setup & Prerequisites

### 1. Verification
Before starting, ensure you have the following installed and configured locally:
*   **Blade CLI (8.0.1+):** Liferay Workspace tooling.
*   **Liferay Docker Manager (LDM):** Local container orchestrator.
*   **GitHub CLI (`gh`):** Logged in (`gh auth status`) and configured for Git operations.
*   **Python (3.10+):** Available in your shell PATH (`python --version`).
*   **Playwright:** Python library installed (`pip install playwright` followed by `playwright install`).

### 2. Enable Required Feature Flags
To use all of the advanced features of Liferay Demo Agents (such as the MCP Server, Page Management REST API, and New CMS), you must enable Liferay's developer feature flags.

Add the following to your local LDM project's `/common/portal-ext.properties` file:

```properties
#LPD-63311 Enables the MCP Server
feature.flag.LPD-63311=true
#LPD-34594 and LPD-17564 together enable the new CMS
feature.flag.LPD-34594=true
feature.flag.LPD-17564=true
#LPD-35443 enables the Page Management API
feature.flag.LPD-35443=true
```

### 3. Auto-Initialization
The framework provides an automated workspace scaffolding utility. When starting a fresh project, running `/lda:init` will:
1.  Scaffold a new LDM container stack and Blade Workspace.
2.  Run `scaffold-workspace.py` to create specs directories, standard `DEMO_PLAN.md` templates, and configure `.gitignore` exclusions.
3.  Automatically extract default administrator credentials from LDM's properties and generate your local `.env` configuration.
4.  Run `provision-agent-admin.py` to programmatically create a dedicated AI Agent administrator account (`shirley.temple@liferay.com`) via headless REST APIs and save her credentials in your local `.env`.

---

## 📥 Installation & Linking

You can install and register this extension in your global **Gemini CLI** configuration using one of the following methods:

### Option A: Link Local Path (Recommended if you want to develop LDA)
If you are developing or modifying the extension, you should link it locally so that any changes are instantly reflected in your active CLI sessions:

1.  **Clone the Repository:**
    Clone/check out the repository to your local machine and navigate into the folder:
    ```bash
    git clone https://github.com/lr-timbraun/liferay-demo-agents.git
    cd liferay-demo-agents
    ```
2.  **Link the Extension:**
    Execute the link command using a relative path (`.`) from inside the cloned directory (or provide the absolute path of your custom local clone):
    ```bash
    gemini extensions link .
    ```

### Option B: Install from Git (Recommended for general use)
To install the extension directly from the remote GitHub repository without a local clone:
```bash
gemini extensions install https://github.com/lr-timbraun/liferay-demo-agents
```

### 🔍 Verify Installation
Verify that the extension has been successfully registered and enabled:
```bash
gemini extensions list
```
You should see `liferay-demo-agents` listed in the output!

---

## 🔄 The Demo Lifecycle Workflow

### Phase 1: Centralized Planning (Orchestrator)
The primary agent acts as the solution architect and does NOT write any code:
1.  **Scrapes Homepage:** Uses the `playwright-scraper` skill to fetch the customer's homepage for style and brand context.
2.  **Interviews User:** Asks for the prospect's identity, narrative, personas, and key "Wow" moments.
3.  **Drafts `DEMO_PLAN.md`:** Creates a high-level roadmap covering the full site experience (homepage, global elements, menu, login) inside `liferay/specs/DEMO_PLAN.md`.
4.  **Writes Technical Specs (`liferay/specs/`):** Defines the strict schemas, CSS tokens, and interface contracts for the sub-agents.
5.  **Defines `liferay/specs/TEST_PLAN.md`:** Outlines the exact frontend validation flows to be executed post-deployment.

### Phase 2: Independent Execution (Delegation)
The Orchestrator invokes the `generalist` sub-agent for each independent component, instructing it to adopt a specific persona:
*   **`site-design-agent`:** Establishes the visual identity (Stylebook JSONs, Global CSS).
*   **`fragment-agent`:** Builds the layout and form fragments (`index.html`, `index.css`, `index.js`, `configuration.json`).
*   **`object-agent`:** Creates Liferay Objects and populates them with realistic, industry-specific data.
*   **`custom-element-agent`:** Implements React-based Custom Element Client Extensions.

### Phase 3: Build, Validation & Delivery (Orchestrator)
The Orchestrator resumes control to deliver and verify the solution:
1.  **Compiles & Hot-Deploys Client Extensions:** Runs `python scripts/deploy-client-extensions.py` from the project directory. This compiles any custom frontend extensions locally for maximum speed and hot-deploys them into LDM's mounted directories.
2.  **Packages & Imports Page Fragments:** Runs `python scripts/deploy-fragments.py` to package fragment collections into ZIPs and automates their browser-based UI import into Liferay's **Global Site** via Playwright.
3.  **Packages & Imports Stylebooks:** Runs `python scripts/deploy-stylebook.py` to package Stylebook token JSONs into ZIPs and automates their browser-based UI import into Liferay's **target Site** via Playwright.
4.  **Verifies Total Setup:** Writes and executes Playwright scripts (`frontend-validation` skill) on the live site, capturing in-flow screenshots of key interaction and data states.
5.  **Generates `tests/TEST_REPORT_<timestamp>.md`:** Delivers a complete validation audit containing descriptions and screenshots of every persona use case.

---

## 🎨 Token Mapping & Styling

To ensure fragments and client extensions are completely portable and support Liferay's **Stylebooks**, sub-agents must strictly follow the **`TOKEN_MAPPING_GUIDE.md`** reference.
*   **Var Mandate:** Always use `var(--token-name)` for CSS rules where a matching Classic theme token is defined.
*   **No Hardcoding:** Hardcoded hex values, RGB strings, or fixed spacer pixels are strictly forbidden.
*   **Interactive States:** When customizing components (like buttons), you must also map their hover/active states (e.g., `btn-primary-hover-background-color`) to ensure a seamless visual transformation.

---

## 🤖 Local Automation Scripts

This framework provides a suite of local Python helper scripts inside the `scripts/` directory to completely automate setup, credentials, and packaging:

*   **`scripts/env_utils.py`:** Secure credentials utility providing modular, on-demand getters for `LIFERAY_HOST`, `LIFERAY_ADMIN_EMAIL_ADDRESS`, and `LIFERAY_ADMIN_PASSWORD` (reads from local `.env`).
*   **`scripts/scaffold-workspace.py`:** Automatically configures LDM project metadata, enables MCP server flags in portal properties, scaffolds `specs/` and `input/` directories, and configures `.gitignore` exclusions.
*   **`scripts/provision-agent-admin.py`:** Automates headless API account provisioning for the dedicated Shirley Temple agent admin user and updates `.env`.
*   **`scripts/deploy-client-extensions.py`:** Locates, builds, zips, and deploys custom client extensions directly to LDM's hot-deploy path.
*   **`scripts/deploy-fragments.py`:** Packages custom fragment collections and uses headless Playwright-RPA browser automation to log in and import them globally.
*   **`scripts/deploy-stylebook.py`:** Packages stylebook token JSONs into Liferay-compliant ZIPs and uses headless Playwright-RPA browser automation to log in and import them to the target Site.

---

## 📄 License
This agent framework is released under the [MIT License](LICENSE). It is intended for creating Demo systems, not for production environments.
