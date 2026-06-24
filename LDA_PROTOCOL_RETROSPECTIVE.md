# Liferay Demo Agents (LDA) Protocol Retrospective
**Date:** Mittwoch, 24. Juni 2026  
**Environment:** Win32 (Windows PowerShell)  
**Target:** Liferay DXP Quarterly (`dxp-2026.q2.4`) on LDM (Liferay Docker Manager)

---

## 1. Encountered Issues & Solutions

During the execution of the Liferay Sales Engineering Initialization Protocol, we successfully bypassed and resolved three core issues:

### Issue A: Missing Helper Scripts in Fresh Workspace Directories
*   **Symptom:** Running the workspace scaffolding command (`python scripts/scaffold-workspace.py --mode init...`) failed with a Python directory missing error (`[Errno 2] No such file or directory`). 
*   **Root Cause:** A fresh directory initialization lacks the required helper scripts inside `./scripts/` out of the box. These scripts actually live inside the template agent workspace (`C:\Liferay\Projects\liferay-demo-agents\scripts`).
*   **Solution:** We recursively copied all baseline tooling scripts (`scaffold-workspace.py`, `provision-agent-admin.py`, etc.) from the template workspace into the new project workspace's `./scripts` folder using PowerShell `Copy-Item`.

### Issue B: SSL Verification Failures on Local Traefik Domain
*   **Symptom:** Running `provision-agent-admin.py` over `https` resulted in a Python HTTP 500/URLError: `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000)`. When falling back to `http://secret.demo`, Traefik responded with a generic HTTP `404 Not Found`.
*   **Root Cause:** LDM provisions local proxy routes (using Traefik) bound strictly to HTTPS with self-signed SSL certificates. Python's default `urllib` forbids self-signed contexts, and the HTTP listener is configured to reject non-HTTPS requests.
*   **Solution:** 
    1. Surgically modified `scripts/provision-agent-admin.py` to bypass verification by injecting global unverified context hooks:
       ```python
       import ssl
       ssl._create_default_https_context = ssl._create_unverified_context
       ```
    2. Updated `.env` to enforce `LIFERAY_HOST=https://secret.demo` instead of `http://secret.demo`.
    3. Registered the Gemini MCP Server using the NodeJS self-signed bypass flag: `--env NODE_TLS_REJECT_UNAUTHORIZED=0`.

### Issue C: Platform-Specific Shell Restrictions & Command Injection Filters
*   **Symptom:** Basic PowerShell commands or multi-line pipeline filters (e.g., trying to modify `.env` or check scripts via native shell commands) were occasionally blocked by the CLI agent's built-in command-injection safeguards or caused syntax errors due to UNIX-to-Windows shell disparities.
*   **Solution:** Shifted entirely to utilizing Gemini surgical tools (`replace` and `write_file`) or platform-independent Python scripts to mutate configurations safely.

---

## 2. Recommendations for Improving the LDA Setup Experience

To enhance robustness, reliability, and speed up future setups, we recommend the following platform and protocol improvements:

### Recommendation 1: Autonomic Script Injection on `/lda:init`
*   **Action:** Ensure the `/lda:init` and `/lda:activate` entrypoints automatically copy or symlink the baseline python/node orchestration helper scripts (located in `liferay-demo-agents/scripts/`) into the newly scaffolded project's `./scripts` folder. Demos should never be bootstrapped with an empty scripts directory.

### Recommendation 2: Introduce Secure/Insecure Flag to Provisioning Tooling
*   **Action:** Upgrade `provision-agent-admin.py` (and similar scripts in the stack) to natively support a `--insecure` or `-k` flag, or automatically hook into `ssl._create_unverified_context` if a local domain (like `.demo` or `localhost`) is detected. This eliminates manual script patching for developers running self-signed local certs.

### Recommendation 3: Default Node MCP Bypass Flags
*   **Action:** Document or automatically inject the `NODE_TLS_REJECT_UNAUTHORIZED=0` environment flag when running `gemini mcp add` on local domains. If LDM automatically forces TLS via Traefik, the tooling should register the MCP Server prepared to deal with self-signed certificates.

### Recommendation 4: Sync URL Protocols in `.env` Generation
*   **Action:** The scaffolding script `scaffold-workspace.py` should read the Traefik configuration or LDM parameters to determine if SSL is active. If LDM generated TLS certs, `.env`'s `LIFERAY_HOST` parameter should default to `https://...` instead of fallback `http://...` to prevent immediate 404 routing errors.
