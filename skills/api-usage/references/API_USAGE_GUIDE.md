# Guide: Liferay Headless REST API Integration

This reference guide details standard HTTP headers and endpoints required to securely consume Liferay DXP services.

---

## 1. Authentication Headers

All API requests must pass basic or OAuth2 bearer authorization tokens loaded from the active profile:

```text
Authorization: Basic admin-user-credentials
Accept: application/json
Content-Type: application/json
```

---

## 2. Standard Endpoint Targets

*   **Dynamic Headless Delivery:** `/o/headless-delivery/v1.0/sites/{siteId}/structured-contents`
*   **Custom Liferay Objects:** `/o/c/{objectDefinitionKey}`
*   **Administrative User Scopes:** `/o/headless-admin-user/v1.0/accounts`
