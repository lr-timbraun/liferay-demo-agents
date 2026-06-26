# Implementation Plan: Native Liferay API Proxy Tools

## Objective
To eliminate the need for Gemini CLI session restarts, we will replace the reliance on Liferay's dynamically loaded MCP Server with a native Gemini CLI JavaScript extension (`index.js`). This extension will statically register the three core Liferay API wrapper tools at startup and dynamically route their executions to the active project's LDM instance.

## Key Files & Context
*   **`package.json`:** Required to define the Node.js project and dependencies (`dotenv`, `node-fetch`).
*   **`index.js`:** The core Gemini CLI extension entry point that registers and handles the native tool executions.
*   **`commands/lda/init.toml` & `commands/lda/activate.toml`:** The prompt protocols that currently instruct the agent to register the MCP server.

## Implementation Steps

### 1. Initialize Node.js Environment
*   Run `npm init -y` to generate a standard `package.json`.
*   Run `npm install dotenv` (to easily parse local project `.env` files).
*   Run `npm install node-fetch` (if necessary for Node < 18 compatibility, though modern Node versions include native `fetch`, we will use native fetch if possible to keep dependencies light).

### 2. Implement `index.js` Proxy Plugin
Create `index.js` exporting the three required static tool declarations for Gemini CLI:
1.  **`liferay_get_openapis`**: Fetches the top-level Liferay API directory.
2.  **`liferay_get_openapi`**: Fetches the OpenAPI specification for a specific endpoint path.
3.  **`liferay_call_http_endpoint`**: Executes a standard HTTP method (GET, POST, PUT, DELETE, PATCH) against a specific endpoint with a JSON payload.

**Execution Logic within each tool:**
*   At execution time (not startup time), the plugin will dynamically read the `.env` file located in the user's *current working directory* (the active demo project).
*   It will extract `LIFERAY_HOST`, `LIFERAY_ADMIN_EMAIL_ADDRESS`, and `LIFERAY_ADMIN_PASSWORD`.
*   It will construct the Basic Auth header and the target URL.
*   It will execute the HTTP request (disabling SSL verification `rejectUnauthorized: false` to support local LDM Traefik certs) and return the JSON response directly to the LLM.

### 3. Clean up Prompt Protocols
*   Remove the steps in `init.toml`, `activate.toml`, and `resume.toml` that instruct the agent to run `gemini mcp add`. The MCP connection will no longer be necessary, as the native tools will handle communication.

## Verification & Testing
1.  Run `/lda:init` in a fresh test directory.
2.  Verify that the container boots and the Shirley Temple account is provisioned.
3.  Immediately, in the same conversational turn, attempt to call the newly registered native `liferay_get_openapis` tool.
4.  Verify that the tool successfully reads the newly generated `.env` file, routes the request to the running container, and returns the API directory JSON.