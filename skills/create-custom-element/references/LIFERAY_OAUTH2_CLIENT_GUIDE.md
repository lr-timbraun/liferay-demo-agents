# Liferay OAuth2.0 Client and Security Guide for Custom Elements

This guide details how to securely configure and execute authenticated API calls from within Liferay Custom Element Client Extensions (React-based) using Liferay's built-in OAuth2.0 system.

---

## 1. Defining the User Agent OAuth2 Application

To authorize your React application to make Headless API calls on behalf of the logged-in user, you must define an `oAuthApplicationUserAgent` entry directly inside your `client-extension.yaml` file.

You must then link this OAuth2 configuration to your custom element using the `oAuth2ApplicationExternalReferenceCode` property.

### Example: `client-extension.yaml`
```yaml
assemble:
    - from: build/static
      into: static

my-react-dashboard:
    name: My React Dashboard
    type: customElement
    friendlyURLMapping: my-react-dashboard
    htmlElementName: my-react-dashboard
    instanceable: true
    oAuth2ApplicationExternalReferenceCode: my-oauth-app-user
    portletCategoryName: category.client-extensions
    urls:
        - js/main.*.js
    cssUrls:
        - css/main.*.css
    useESM: true

my-oauth-app-user:
    name: My React Dashboard OAuth Application
    type: oAuthApplicationUserAgent
    homePageURL: http://localhost:8080
    scopes:
        - Liferay.Object.REST.everything
        - Liferay.Headless.Admin.User.everything
```
*   **`oAuth2ApplicationExternalReferenceCode`**: Maps the custom element to the authorized OAuth2 user agent.
*   **`homePageURL`**: MUST include the protocol and domain (e.g., `http://localhost:8080`) to prevent NullPointerException crashes during Liferay's deployment interpolation.
*   **`scopes`**: Define the specific scopes/permissions your React app requires.

---

## 2. Dynamic Token-Safe Fetching (Liferay.Util.fetch)

When your React custom element runs inside a Liferay Page, Liferay automatically handles the active session and injects OAuth2 token contexts for you.

You do NOT need to write manual authentication or token-exchange loops. Instead, you MUST use the global **`Liferay.Util.fetch()`** utility to perform headless REST API requests.

### Key Benefits of `Liferay.Util.fetch()`:
1.  **Automatic Token Injection:** Automatically fetches and appends the active OAuth2 JWT Bearer token into the `Authorization` header.
2.  **CSRF Protection:** Automatically appends Liferay's active CSRF token (`p_auth`) to protect state-changing requests (POST, PUT, DELETE).
3.  **Automatic Token Refresh:** Automatically handles token expiration and renews keys silently in the background.

### Standard Fetch Boilerplate in React:
```javascript
/* global Liferay */
import React, { useState, useEffect } from 'react';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(True);
    const [error, setError] = useState(None);

    useEffect(() => {
        // Use Liferay's native fetch utility for authenticated requests
        if (typeof Liferay !== 'undefined' && Liferay.Util && Liferay.Util.fetch) {
            Liferay.Util.fetch('/o/headless-commerce-delivery-catalog/v1.0/products')
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    setProducts(data.items || []);
                    setLoading(False);
                })
                .catch(err => {
                    setError(err.message);
                    setLoading(False);
                });
        } else {
            setError("Liferay platform APIs are not available.");
            setLoading(False);
        }
    }, []);

    if (loading) return <div>Loading products...</div>;
    if (error) return <div className="alert alert-danger">Error: {error}</div>;

    return (
        <ul>
            {products.map(p => (
                <li key={p.id}>{p.name}</li>
            ))}
        </ul>
    );
};

export default ProductList;
```

---

## 3. External Microservice Calls (The ES6 OAuth2Client Module)

If your React custom element needs to call an external API or microservice (such as a Node.js server-side Client Extension deployed on Liferay Cloud), you must still authenticate the Liferay user securely.

You can import Liferay's native OAuth2 Client module to automatically manage tokens and make secure calls to external microservices.

### Step 1: Import the Module
At the top of your component or JS file, import the module:
```javascript
import * as OAuth2Client from '@liferay/oauth2-provider-web/client';
```

### Step 2: Initialize and Execute Fetches
Initialize the client using the OAuth External Reference Code (ERC) and use its `.fetch()` utility to execute requests:
```javascript
const makeSecureExternalCall = async (payload) => {
    try {
        // Initialize the client using the OAuth application ERC
        const oauth2Client = await OAuth2Client.FromUserAgentApplication('my-oauth-app-user');

        // Use the client's fetch method to hit your external microservice
        const data = await oauth2Client.fetch('https://my-external-api.lfr.cloud/api/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        // IMPORTANT: oauth2Client.fetch() automatically parses the JSON body for you.
        // It returns the parsed data object directly, NOT a standard raw Response.
        if (data && data.error) {
            throw new Error(`API Error: ${data.error}`);
        }

        return data;
    } catch (err) {
        console.error('External API Request Failed:', err);
        throw err;
    }
};
```

---

## 4. ESLint & Build Troubleshooting

React-scripts is highly strict regarding global variables and syntax validation during build operations.

1.  **Global Liferay Reference:** Always add `/* global Liferay */` at the very top of your source files when referencing `Liferay` to prevent compiler/ESLint failures.
2.  **Unexpected token `<` Error:** If Liferay serves raw JSX in the browser and triggers parsing errors, verify your `assemble` block in `client-extension.yaml`. This error means Liferay is trying to serve the raw `src/index.js` instead of the transpiled production bundle located under `build/static/`.
