# Liferay User, B2B Account, and Organization Onboarding Guide

This guide details how to programmatically onboarding business accounts, configure multi-level organization hierarchies, define strict postal addresses, link users, and flatten scoped roles inside React components.

---

## 1. B2B Business Accounts

B2B transactional systems in Liferay require Accounts to manage corporate contracts, catalogs, and checkout.

### A. Create the Account
*   **Endpoint:** `POST /o/headless-admin-user/v1.0/accounts`
*   **Payload:**
    ```json
    {
        "name": "Acme Pharmaceuticals Ltd",
        "type": "business"
    }
    ```

### B. Add a Postal Address (Country/Region Guard)
Liferay DXP has strict internal validation dictionaries for addresses. Mismatched strings will trigger a `400 BAD REQUEST` error.

*   **Endpoint:** `POST /o/headless-admin-user/v1.0/accounts/{accountId}/postal-addresses`
*   **Validation Rules:**
    1.  **`addressCountry`**: Must match the explicit country name in Liferay exactly (e.g. `"United Kingdom"`, not `"GB"`).
    2.  **`addressRegion`**: Must perfectly match Liferay's region dictionary. For the UK, this is highly specific (e.g. `"London, City of"`, not `"Greater London"`).
    3.  **`addressType`**: Must match a Liferay List Type in lowercase (e.g. `"billing"`, `"shipping"`).
*   **Script Safeguard:** You MUST wrap your address attachment blocks inside a `try/catch` block so that any regional dictionary mismatch does not crash the entire onboarding flow.

*   **Payload:**
    ```json
    {
        "addressCountry": "United Kingdom",
        "addressRegion": "London, City of",
        "addressType": "billing",
        "city": "London",
        "name": "Acme Billing Address",
        "street1": "100 Wood Street",
        "zip": "EC2V 7AN"
    }
    ```

---

## 2. Organization Hierarchies

Organizations in Liferay represent location-based, corporate, or division-based reporting structures. They are used to scope content, permissions, pages, and document access.

### A. Create an Organization
*   **Endpoint:** `POST /o/headless-admin-user/v1.0/organizations`
*   **Payload:**
    ```json
    {
        "name": "Acme North America Division"
    }
    ```

### B. Create a Sub-Organization
To build multi-level hierarchies, link child organizations to parents using the `parentOrganizationId` key:

*   **Endpoint:** `POST /o/headless-admin-user/v1.0/organizations`
*   **Payload:**
    ```json
    {
        "name": "Acme New York Office",
        "parentOrganizationId": 12345
    }
    ```

---

## 3. Linking Users and Mapping Roles

Once accounts or organizations are created, associate user accounts and assign scoped role permissions.

### A. Associate User to Account
*   **Endpoint:** `POST /o/headless-admin-user/v1.0/accounts/{accountId}/user-accounts/by-email-address/{userEmail}`

### B. Associate User to Organization
*   **Endpoint:** `POST /o/headless-admin-user/v1.0/organizations/{organizationId}/user-accounts/by-email-address/{userEmail}`

### C. Assign Scoped B2B Account Roles
Assign roles (like Account Administrator or custom B2B buyer roles) by their External Reference Code (ERC) relative to the user account:

*   **Endpoint:** `POST /o/headless-admin-user/v1.0/accounts/{accountId}/account-roles/by-external-reference-code/ACCOUNT_ADMINISTRATOR/user-accounts/{userId}`

---

## 4. Flattening Scoped Roles in React Components

When retrieving a user's role profile (via `/o/headless-admin-user/v1.0/my-user-account`), Liferay scopes roles by context (e.g., Site-scoped, Account-scoped, Organization-scoped).

To cleanly evaluate if a user is authorized for B2B buyer actions or dealer-specific custom dashboards, your React components MUST flatten all possible brief scopes:

```javascript
const userUrl = '/o/headless-admin-user/v1.0/my-user-account';
const userData = await Liferay.Util.fetch(userUrl).then(res => res.json());

// Flatten all possible contextual role briefs
const allRoles = [
    ...(userData.roleBriefs || []), // Global
    ...(userData.accountBriefs || []).flatMap(acc => acc.roleBriefs || []), // Account-scoped
    ...(userData.organizationBriefs || []).flatMap(org => org.roleBriefs || []), // Org-scoped
    ...(userData.siteBriefs || []).flatMap(site => site.roleBriefs || []), // Site-scoped
    ...(userData.userGroupBriefs || []).flatMap(ug => ug.roleBriefs || []) // User-group-scoped
];

// Verify if user is authorized for B2B Account Admin actions
const isAccountAdmin = allRoles.some(role => role.name === 'Account Administrator');
```
