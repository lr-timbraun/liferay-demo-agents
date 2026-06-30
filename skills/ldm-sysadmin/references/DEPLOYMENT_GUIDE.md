# Guide: LDM System Administration & Deployment Feedback

This reference guide provides deep, real-world domain knowledge and feedback interpretations for automating Liferay DXP Page Fragment, Style Book, and Client Extension deployments inside local Liferay Docker Manager (LDM) stacks.

---

## 🚀 Execution & Command Reference

### 1. Page Fragments Deployer (`deploy-fragments.py`)
This script automates compiling, packaging, and importing Page Fragment collections into the Global Site using Playwright RPA.

*   **Location:** `./scripts/deploy-fragments.py`
*   **Execution Command:**
    ```bash
    python scripts/deploy-fragments.py
    ```
*   **Actions Performed:**
    1. Scan `./liferay/fragments/` for collections containing `collection.json`.
    2. Package each collection into a ZIP file in `./liferay/dist/`.
    3. Log into Liferay at `LIFERAY_HOST` using `.env` credentials.
    4. Open the Global Site's Page Fragments panel and trigger the import sub-page.
    5. Upload the ZIP file and handle duplication collisions automatically.
    6. Wait for modal fade-outs, capture a standardized visual receipt, extract DXP feedback, and close.

### 2. Style Books Deployer (`deploy-stylebook.py`)
This script automates compiling, packaging, and importing Style Book files into a target Liferay Site.

*   **Location:** `./scripts/deploy-stylebook.py`
*   **Execution Command (with site Friendly URL path):**
    ```bash
    python scripts/deploy-stylebook.py --site guest
    ```
*   **Actions Performed:**
    1. Scan `./liferay/stylebooks/` for folders containing `style-book.json`.
    2. Package each folder with subdirectory-nesting (critical for DXP keys) into a ZIP in `./liferay/dist/`.
    3. Log into Liferay and navigate to the target site's Style Books panel:
       `{LIFERAY_HOST}/group/{site}/~/control_panel/manage/-/style_books/style_books`
    4. Click Liferay's global Control Menu header Actions button and select standalone Import, bypassing "Export / Import".
    5. Upload the ZIP, submit inside the iframe, capture a standardized visual receipt of the alerts, and close.

### 3. Client Extensions Deployer (`deploy-client-extensions.py`)
This script automates compiling, packaging, and hot-deploying Client Extensions directly inside LDM container stacks.

*   **Location:** `./scripts/deploy-client-extensions.py`
*   **Execution Command:**
    ```bash
    python scripts/deploy-client-extensions.py
    ```
*   **Actions Performed:**
    1. Scan `./liferay/client-extensions/` for folders containing `client-extension.yaml`.
    2. Trigger Liferay's native Gradle wrapper build (**`gradlew clean build`**) inside `./liferay/` to compile Node/React assets and bundle them into 100% compliant LUFFA archives.
    3. Dynamically search each extension subproject's `build/` folder for the compiled `.zip` file.
    4. Copy the found, Gradle-built ZIP files into LDM's root hot-deploy path: `./client-extensions/`.
    5. Programmatically trigger **`ldm deploy`** to synchronize built assets and refresh the active container stack!

---

## 📊 Standardized Visual Audit Receipts

All automated imports write high-resolution screenshot receipts to document successful execution and surface warning alerts visually.

### Storage Location:
*   Saved inside the local, `.gitignore`'d directory:
    **`./liferay/dist/receipts/`**

### File Naming Convention:
```text
receipt_{resource_type}_{resource_name}_{YYYYMMDD_HHMMSS}_{status_descriptor}.png
```
*   **`resource_type`:** `fragments` or `stylebook`
*   **`resource_name`:** Folder name of the imported asset (e.g. `elo-components`, `elo-brand-stylebook`).
*   **`YYYYMMDD_HHMMSS`:** Precise execution timestamp.
*   **`status_descriptor`:**
    *   `success`: Clear, error-free import.
    *   `success_warnings`: Imported successfully, but Liferay surfaced non-blocking warnings on screen.
    *   `failure`: Hard, critical failure preventing completion.

---

## 🔍 Understanding & Handling Liferay DXP Feedback

Through active live-test experiences, we have mapped Liferay DXP's response layouts and how to handle them cleanly:

### 1. Duplication Conflicts ("Manage Existing Items")
*   **DXP Behavior:** When importing a fragment set that already exists in the list, Liferay opens a centered `"Manage Existing Items"` modal overlay asking the user to choose an action.
*   **Script Handling:** The deployer script actively monitors for this modal. It selects the language-independent radio option **`value="overwrite"`** and clicks **`Save`** inside the modal footer to cleanly overwrite the items.
*   **Receipt Capture:** To avoid capturing a semi-transparent, ugly fading backdrop overlay, the script waits for `.modal-dialog` and `.modal-backdrop` to be completely hidden (`state="hidden"`) with a `1000ms` safety pause before snapping the screenshot.

### 2. Theme Mismatch Warnings (`.alert-warning`)
*   **DXP Behavior:** When importing a Style Book, Liferay DXP compares the Style Book's target SASS variables with the active theme of your site. If they differ (e.g., Style Book targets Classic `classic_WAR_classictheme` but the site runs a custom theme), Liferay displays a yellow warning alert:
    > `"warning:One or more of the style books are based on a theme that is different from the site's default theme..."`
*   **Crucial Knowledge:** **This warning is NOT a critical failure.** Liferay actually completes the import successfully and registers the Style Book!
*   **Script Handling:** The deployer parses this and logs it as a non-blocking `⚠️ [WARNING]` block, but allows the script to succeed and exit with code `0`.
*   **Receipt Capture:** Captured **immediately inside the iframe modal** while the warning alert is fully displayed on screen, preserving the visual audit of the warning.

### 3. Critical Failures (`.alert-danger`)
*   **DXP Behavior:** Hard failures (like syntax errors inside JSON schemas, missing properties, or database constraint violations) are surfaced in red `.alert-danger` or `.clay-alert-danger` boxes.
*   **Script Handling:** The deployer intercepts these, extracts the raw DXP validation error text, outputs a detailed `❌ [ERROR]` box to stdout, and terminates with exit code `1` (fail) to trigger self-healing or alert the executing agent.
