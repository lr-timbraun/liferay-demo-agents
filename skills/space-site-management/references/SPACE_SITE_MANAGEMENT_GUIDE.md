# Guide: Liferay Spaces & Sites Provisioning

This reference guide provides standard API routes and payload schemas required to programmatically provision DXP Spaces.

---

## Standard Provisioning Payload

To create a new high-level Asset Library (Space), post this exact JSON structure to Liferay's headless admin site endpoint:

```json
{
  "name": "Acme Global Assets Space",
  "externalReferenceCode": "acme-global-space-erc",
  "description": "High-level Space container for Object-based content and media."
}
```

**Target Endpoint:** `/o/headless-admin-site/v1.0/asset-libraries`
