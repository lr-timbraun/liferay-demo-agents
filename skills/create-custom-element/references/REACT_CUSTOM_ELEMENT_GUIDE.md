# Guide: React Custom Element Client Extensions in Liferay Workspace

This document summarizes the verified configuration and project structure required to successfully build and deploy a React-based Custom Element Client Extension (CX) in a Liferay Workspace.

## 1. Project Structure
The project should follow the standard Create React App (CRA) structure:
```
client-extensions/[project-name]/
├── package.json
├── client-extension.yaml
├── bnd.bnd
├── public/
│   └── index.html
└── src/
    └── index.js
```

## 2. Configuration Files

### `package.json`
Use `react-scripts` for a reliable build process that Liferay Workspace can easily bundle.
```json
{
  "name": "my-react-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
```

### `client-extension.yaml`
Key requirements:
- **Assemble**: Must pull from `build/static` (CRA default) and place `into: static`.
- **URLs**: Use glob patterns (`js/main.*.js`) because CRA appends hashes to filenames.

```yaml
assemble:
    - from: build/static
      into: static

my-react-app:
    name: My React App
    type: customElement
    friendlyURLMapping: my-react-app
    htmlElementName: my-react-app
    instanceable: true
    oAuth2ApplicationExternalReferenceCode: my-oauth-user
    portletCategoryName: category.client-extensions
    urls:
        - js/main.*.js
    cssUrls:
        - css/main.*.css
    useESM: true

my-oauth-user:
    name: My OAuth User Agent
    type: oAuthApplicationUserAgent
    homePageURL: http://localhost:8080
    scopes:
        - Liferay.Object.REST.everything
```

## 3. React Source (`src/index.js`)
- **Global Liferay**: Use `/* global Liferay */` to satisfy ESLint.
- **Cleanup**: Implement `disconnectedCallback` to unmount the React root.

```javascript
/* global Liferay */
import React from 'react';
import { createRoot } from 'react-dom/client';

const App = () => (
    <div className="my-app">
        <h1>Hello from React!</h1>
    </div>
);

class MyCustomElement extends HTMLElement {
    connectedCallback() {
        if (!this.root) {
            this.root = createRoot(this);
        }
        this.root.render(<App />);
    }
    disconnectedCallback() {
        if (this.root) {
            this.root.unmount();
            this.root = null;
        }
    }
}

const ELEMENT_ID = 'my-react-app';
if (!customElements.get(ELEMENT_ID)) {
    customElements.define(ELEMENT_ID, MyCustomElement);
}
```
