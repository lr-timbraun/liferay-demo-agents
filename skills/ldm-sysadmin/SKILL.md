---
name: ldm-sysadmin
description: System administration and asset deployment for Liferay Docker Manager (LDM) workspaces. Use when compiling, packaging, deploying, or verifying Page Fragments, Style Books, or client extensions inside an active local Liferay/LDM stack.
---

# Skill: LDM System Administration & Deployment

This skill provides specialized system administration, automated asset deployment, and feedback diagnostics guidance for local Liferay Docker Manager (LDM) workspaces.

---

## Available Scripts

All deployment scripts are bundled directly within this skill.
- **`scripts/deploy-fragments.py`** — Packages Page Fragment collections and automates browser-based UI imports into Liferay DXP via Playwright.
- **`scripts/deploy-stylebook.py`** — Packages Style Books with unique DXP nesting and automates browser-based UI imports into Liferay DXP via Playwright.
- **`scripts/deploy-client-extensions.py`** — Compiles Node/React/static client extensions and hot-deploys them into LDM container stacks.

---

## Workflows

Always execute these workflows from the active project root workspace directory. To run any script, resolve the skill's root directory path (`<skill_dir>`) from the `<location>` of this skill (`ldm-sysadmin`) in your system prompt.

### 1. Page Fragments Deployment
*   **Action:** Package local page fragments into ZIP archives and import them globally.
*   **Execution Command:**
    ```bash
    python <skill_dir>/scripts/deploy-fragments.py
    ```
*   **Arguments:**
    *   `--host <host_url>` — Override Liferay host URL (defaults to env-resolved URL).
    *   `--email <email>` — Override admin email (defaults to env-resolved email).
    *   `--password <password>` — Override admin password (defaults to env-resolved password).
    *   `--dry-run` — Package collections and validate configurations without executing live browser deployment.
*   **Verification:** Confirm that a green `[SUCCESS]` block is printed to `stdout` with the list of successfully imported elements.

### 2. Style Books Deployment
*   **Action:** Package local Style Books with subdirectory-nesting and import them into a target Site.
*   **Execution Command:**
    ```bash
    python <skill_dir>/scripts/deploy-stylebook.py --site <site_friendly_url_path>
    ```
*   **Arguments:**
    *   `--site <friendly_url>` — Friendly URL path of target site (default: `'guest'`).
    *   `--host <host_url>` — Override Liferay host URL (defaults to env-resolved URL).
    *   `--email <email>` — Override admin email (defaults to env-resolved email).
    *   `--password <password>` — Override admin password (defaults to env-resolved password).
    *   `--dry-run` — Package Style Books and validate configurations without executing live browser deployment.
*   **Verification:** Confirm that a clean success or non-blocking warning block is printed to `stdout`.

### 3. Client Extensions Deployment
*   **Action:** Compile and package local React/Node-based or static client extensions, and hot-deploy them inside the active LDM container stack.
*   **Execution Command:**
    ```bash
    python <skill_dir>/scripts/deploy-client-extensions.py
    ```
*   **Arguments:**
    *   `--dry-run` — Scan projects and validate compilation tool availability without triggering builds or deployment.
*   **Verification:** Confirm that the packaging completes and triggers `ldm deploy` successfully, outputting `"All Liferay Client Extensions deployed and synchronized successfully!"` to stdout.

---

## Deployment Visual Receipts (Visual Audit)

Every deployment run automatically creates a standardized high-resolution visual receipt screenshot to document results on-screen.

### Location on Disk:
*   Saved inside the local, `.gitignore`'d directory:
    **`./liferay/dist/receipts/`**

### Standardized Naming Convention:
`receipt_{resource_type}_{resource_name}_{YYYYMMDD_HHMMSS}_{status_descriptor}.png`
*   `resource_type`: `fragments` or `stylebook`
*   `resource_name`: Folder name of the imported asset (e.g. `elo-components`, `elo-brand-stylebook`).
*   `status_descriptor`: `success`, `success_warnings`, or `failure`.

---

## Understanding & Diagnosing Feedback

Liferay DXP returns various visual feedback states inside its import modals (such as theme mismatches, duplication prompts, or validation alerts). 

### Detailed Feedback Interpretation Guide:
For complete, step-by-step instructions on understanding Liferay's visual output, handling duplication overlays, and parsing theme mismatches, you **MUST** read and load the following reference file:

**[references/DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md)**
