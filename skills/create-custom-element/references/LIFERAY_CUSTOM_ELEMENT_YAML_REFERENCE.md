# Liferay Client Extension YAML Configuration Reference

This reference details the mandatory and optional properties allowed inside `client-extension.yaml` for both `customElement` and `oAuthApplicationUserAgent` Client Extension types.

---

## 1. Global Assembly Block

Every `client-extension.yaml` file must start with a global `assemble` block defining how raw static assets are compiled and packaged into Liferay-ready `.zip` (LUFFA) files.

```yaml
assemble:
    - from: build/static
      into: static
```
*   **`from`**: Directs the compiler to the build output directory of your compilation tool (for Create React App, this is `build/static`).
*   **`into`**: Directs Liferay's static server to host the assets inside the virtual `static/` directory of your deployed container.

---

## 2. Custom Element Configuration (`type: customElement`)

The custom element block defines the front-end widget that Liferay will register as a custom HTML5 Web Component.

### Schema Properties:

| Property Name | Type | Default Value | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `type` | string | | **Yes** | MUST be set to `customElement`. |
| `name` | string | | **Yes** | The user-friendly name displayed in Liferay's Widget sidebar (e.g. "React User Profile"). |
| `htmlElementName` | string | | **Yes** | The custom HTML tag name registered in the browser (e.g. `react-user-profile`). MUST contain a hyphen and match the custom element definition in your JS source. |
| `friendlyURLMapping` | string | | **Yes** | Unique URL route mapper used by Liferay (typically matches the element ID, e.g. `react-user-profile`). |
| `instanceable` | boolean | | **Yes** | Set to `true` to allow multiple instances of this custom element to be placed on a single page. |
| `urls` | array | | **Yes** | List of JavaScript bundle relative paths (relative to `static/` mapping). Supports glob hashing: `js/main.*.js`. |
| `cssUrls` | array | | No | List of CSS relative paths. Supports glob hashing: `css/main.*.css`. |
| `useESM` | boolean | | No | Set to `true` if compiling the React elements to support ES modules (Modern DXP recommendation). |
| `oAuth2ApplicationExternalReferenceCode` | string | | No | The External Reference Code (ERC) of the OAuth2 User Agent application defined in the YAML. Required if making authenticated API calls. |
| `portletCategoryName` | string | `category.client-extensions` | No | Sets where the element appears in Liferay's Page Widget sidebar. |
| `panelCategoryKey` | string | | No | Key of Liferay's Control Panel or Site Menu category where the custom element appears as an application (e.g., `site_administration.content`). Only takes effect when `panelAppOrder` is also set. |
| `panelAppOrder` | integer / string | | No | Order position of the custom element among applications inside its panel category (e.g., `700`). Only takes effect when `panelCategoryKey` is also set. |
| `properties` | string array | `[]` | No | Properties to append as attributes to the custom HTML element. Items are separated by newlines and processed as standard Java properties (e.g. `theme=dark`). |
| `sourceCodeURL` | URL | `https://www.liferay.com` | No | The address to the client extension's source repository. |
| `description` | string | | No | A clear description of the custom element client extension. |

### Example:
```yaml
react-user-profile:
    name: React User Profile
    type: customElement
    friendlyURLMapping: react-user-profile
    htmlElementName: react-user-profile
    instanceable: true
    oAuth2ApplicationExternalReferenceCode: my-oauth-user-agent
    portletCategoryName: category.client-extensions
    panelCategoryKey: site_administration.content
    panelAppOrder: 700
    properties:
        - theme=dark
        - view=compact
    sourceCodeURL: https://github.com/lr-timbraun/liferay-demo-agents
    description: A secure React-based User Profile dashboard with dynamic OAuth2 authentication.
    urls:
        - js/main.*.js
    cssUrls:
        - css/main.*.css
    useESM: true
```

---

## 3. OAuth2 User Agent Configuration (`type: oAuthApplicationUserAgent`)

The User Agent block defines an OAuth2 application used to securely authorize your custom element on behalf of the active logged-in portal user.

### Schema Properties:

| Property Name | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `type` | string | **Yes** | MUST be set to `oAuthApplicationUserAgent`. |
| `name` | string | **Yes** | User-friendly name of the OAuth application. |
| `homePageURL` | string | **Yes** | Home page URL of the Liferay portal. MUST include the protocol and domain (e.g., `http://localhost:8080`) to prevent NullPointerException crashes during deployment. |
| `scopes` | array | **Yes** | Flat array of REST/Object API scopes your React application is authorized to query. |
| `clientSecret` | string | No | Optional static client secret. Typically omitted for User Agent flows to let Liferay manage tokens on-demand. |

### Example:
```yaml
my-oauth-user-agent:
    name: React User Profile OAuth App
    type: oAuthApplicationUserAgent
    homePageURL: http://localhost:8080
    scopes:
        - Liferay.Object.REST.everything
        - Liferay.Headless.Admin.User.everything
```

---

## 4. Standard OAuth2 API Scopes Reference

When defining your User Agent, you must declare exactly which Liferay Headless endpoints your custom element can access:

*   **Custom Objects (Generic Scope):**
    `Liferay.Object.REST.everything` (Provides full CRUD access to all custom Liferay Objects).
*   **User Profiles & Accounts:**
    `Liferay.Headless.Admin.User.everything` (Allows fetching detailed user details, accounts, organizations, and role maps).
*   **Core Portal Content & Files:**
    `Liferay.Headless.Delivery.everything` (Allows fetching documents, folders, site pages, blogs, and unstructured web content).
*   **B2B Commerce Delivery Catalog:**
    `Liferay.Headless.Commerce.Delivery.Catalog.everything` (Allows reading catalog products, SKUs, and categories).
