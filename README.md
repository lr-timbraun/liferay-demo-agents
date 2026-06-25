# Liferay Demo Agent Framework

This repository houses the configuration, specialized agent personas, custom skills, and local automation scripts designed for **Gemini CLI** (and other compatible AI tools) to automate the development, packaging, and validation of Liferay DXP demonstrations.

It is tailored specifically for **Liferay Sales Engineers** to build visually stunning, "Boardroom Ready" proof-of-concepts and demos with speed, consistency, and structural integrity.

---

## 🚀 Key Features

*   **Orchestrator/Sub-Agent Workflow:** Separates strategic planning (Phase 1) from granular implementation (Phase 2) and final delivery/validation (Phase 3).
*   **Specialized Agent Personas:** Dedicated configurations for `site-design`, `fragment`, `object`, and `custom-element` development.
*   **Concurrently Isolated Execution:** Sub-agents are restricted to their assigned directories, enabling multiple agents to run in parallel without file collisions.
*   **End-to-End Persona Validation:** Mandates the creation of a `specs/TEST_PLAN.md` which performs visual, interactive, in-session browser testing on the live site.
*   **Local Python Automation:** Pre-built scripts for zipping stylebooks, packaging fragment collections, and programmatically publishing custom Liferay Objects.

---

## 📁 Repository Structure

```text
.
├── .gemini/               # Gemini CLI configuration
│   ├── agents/            # Specialized sub-agent personas (Markdown)
│   │   ├── site-design-agent.md
│   │   ├── fragment-agent.md
│   │   ├── object-agent.md
│   │   └── custom-element-agent.md
│   └── skills/            # Specialized AI skills (SKILL.md + references/)
│       ├── site-design/       # Stylebooks & Global CSS logic
│       ├── create-fragment/   # UI/Form Fragments & FreeMarker APIs
│       ├── liferay-objects/   # Object schemas & population
│       ├── playwright-scraper/# Customer homepage scraping
│       └── frontend-validation/# Interactive Playwright validation
├── .gitignore             # Ignores build outputs & keeps .env local
├── GEMINI.md              # Project-wide instructions, blocking init protocol, & core mandates
├── REUSABLE_ASSETS.md     # Registry of source repositories for component discovery
├── .env                   # Local credentials template (ignored by Git)
└── scripts/               # Local helper & packaging scripts (not committed to demos)
    ├── liferay_utils.py   # Secure credential & host URL resolver
    ├── create-object-definition.py # Automates Object creation & publishing
    ├── package-fragments.py  # Strict ZIP bundler for Fragment collections
    ├── package-stylebook.py  # Strict ZIP bundler for Stylebooks
    └── get_dom.py         # Playwright scraper utility
```

---

## 🛠️ Setup & Prerequisites

### 1. Verification
Before starting, ensure you have the following installed and configured locally:
*   **GitHub CLI (`gh`):** Logged in (`gh auth status`) and configured for standard Git operations (`gh auth setup-git`).
*   **Python (3.10+):** Installed and available in your shell PATH (`python --version`).
*   **Playwright:** Python library installed (`pip install playwright` followed by `playwright install`).

### 2. Configure Liferay Admin Credentials
The framework includes an automated credential utility (`scripts/liferay_utils.py`) that searches upwards for a local `.env` file. 

Create a `.env` file in the project root containing your Liferay user credentials (a dedicated AI account like `ai-agent@liferay.com` is highly recommended for audit trail clarity):

```text
LIFERAY_ADMIN_EMAIL_ADDRESS=ai-agent@liferay.com
LIFERAY_ADMIN_PASSWORD=your-secure-password
```

---

## 🔄 The Demo Lifecycle Workflow

### Phase 1: Centralized Planning (Orchestrator)
The primary agent acts as the solution architect and does NOT write any code:
1.  **Scrapes Homepage:** Uses the `playwright-scraper` skill to fetch the customer's homepage for style and brand context.
2.  **Interviews User:** Asks for the prospect's identity, narrative, personas, and key "Wow" moments.
3.  **Drafts `DEMO_PLAN.md`:** Creates a high-level roadmap covering the full site experience (homepage, global elements, menu, login).
4.  **Writes Technical Specs (`specs/`):** Defines the strict schemas, CSS tokens, and interface contracts for the sub-agents.
5.  **Defines `specs/TEST_PLAN.md`:** Outlines the exact frontend validation flows to be executed post-deployment.

### Phase 2: Independent Execution (Delegation)
The Orchestrator invokes the `generalist` sub-agent for each independent component, instructing it to adopt a specific persona:
*   **`site-design-agent`:** Establishes the visual identity (Stylebook JSONs, Global CSS).
*   **`fragment-agent`:** Builds the layout and form fragments (`index.html`, `index.css`, `index.js`, `configuration.json`).
*   **`object-agent`:** Creates the Objects and populates them with realistic, industry-specific data.
*   **`custom-element-agent`:** Implements React-based Custom Element Client Extensions.

### Phase 3: Build, Validation & Delivery (Orchestrator)
The Orchestrator resumes control to deliver and verify the solution:
1.  **Compiles & Packages:** Runs `package-fragments.py` and `package-stylebook.py` to create the ZIP archives. Pushes Client Extension code to GitHub to trigger the Liferay PaaS build.
2.  **Guides Deployment:** Instructs the user to trigger manual deployment in the PaaS console.
3.  **Verifies Total Setup:** Upon explicit user request, writes and executes Playwright scripts (`frontend-validation` skill) on the live site, capturing in-flow screenshots of key interaction and data states.
4.  **Generates `TEST_REPORT_<timestamp>.md`:** Delivers a complete validation audit containing descriptions and screenshots of every persona use case.

---

## 🎨 Token Mapping & Styling

To ensure fragments and client extensions are completely portable and support Liferay's **Stylebooks**, sub-agents must strictly follow the **`TOKEN_MAPPING_GUIDE.md`** reference.
*   **Var Mandate:** Always use `var(--token-name)` for CSS rules where a matching Classic theme token is defined.
*   **No Hardcoding:** Hardcoded hex values, RGB strings, or fixed spacer pixels are strictly forbidden.
*   **Interactive States:** When customizing components (like buttons), you must also map their hover/active states (e.g., `btn-primary-hover-background-color`) to ensure a seamless visual transformation.

---

## 📄 License
This agent framework is intended for Liferay Sales Engineering internal use.
