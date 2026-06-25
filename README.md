# Liferay Demo Agent Framework

This repository houses the configuration, specialized agent personas, custom skills, and local automation scripts designed for **Gemini CLI** (and other compatible AI tools) to automate the development, packaging, and validation of Liferay DXP demonstrations locally using **Liferay Docker Manager (LDM)** and **Blade CLI**.

It is tailored specifically for building visually stunning, "Boardroom Ready" proof-of-concepts and demos with speed, consistency, and structural integrity.

---

## 🚀 Key Features

*   **Orchestrator/Sub-Agent Workflow:** Separates strategic planning (Phase 1) from granular implementation (Phase 2) and final delivery/validation (Phase 3).
*   **Specialized Agent Personas:** Dedicated configurations for `site-design`, `fragment`, `object`, and `custom-element` development. Further agents are in development.
*   **Concurrently Isolated Execution:** Sub-agents are restricted to their assigned directories, enabling multiple agents to run in parallel without file collisions.
*   **Automated Deployment Scripts:** A suite of local Python scripts that automate compiling, packaging, and hot-deploying Stylebooks, Fragments, and Client Extensions.
*   **End-to-End Persona Validation:** Mandates the creation of a `liferay/specs/TEST_PLAN.md` which performs visual, interactive, in-session browser testing on the live site.

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

## 🛠️ Project Setup & Prerequisites

### 1. Verification
Before starting, ensure you have the following installed and configured locally:
*   **Blade CLI (8.0.1+):** Liferay Workspace tooling.
*   **Liferay Docker Manager (LDM):** Local container orchestrator.
*   **Python (3.10+):** Available in your shell PATH (`python --version`).
*   **GitHub CLI (`Optional, only required if you plan to use a github repository`):** Logged in (`gh auth status`) and configured for Git operations.
*   **Playwright:** Python library installed (`pip install playwright` followed by `playwright install`).

LDA will automatically check if these have been installed and won't initialize projects without them.

### 2. Enable Required Feature Flags
To use all of the advanced features of Liferay Demo Agents (such as the MCP Server, Page Management REST API, and New CMS), you must enable Liferay's developer feature flags.

Add the following to your LDM `/common/portal-ext.properties` file:

```properties
#LPD-63311 enables the MCP Server
feature.flag.LPD-63311=true
#LPD-34594 and LPD-17564 together enable the new CMS
feature.flag.LPD-34594=true
feature.flag.LPD-17564=true
#LPD-35443 enables the Page Management API
feature.flag.LPD-35443=true
```

### 3. Auto-Initialization
Create an empty directory, open your Gemini CLI in it, and run the following command:

```bash
/lda:init
```

If you already have an LDM Project, you can add LDA to it by using

```bash
/lda:activate
```

### 4. Continuing your work (Experimental)
> ⚠️ **EXPERIMENTAL:** This feature is currently experimental and in active development.

To continue where you left off before, you can run:

```bash
/resume     # This will resume your previous gemini session
/lda:resume # This will bring back up the LDM containers
```

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

## 📄 License
This agent framework is released under the [MIT License](LICENSE). It is intended for creating Demo systems, not for production environments.
