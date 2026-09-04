# Guide: Liferay B2B Accounts & Organizations Onboarding

This reference guide details standard Headless endpoint targets and JSON payload structures required to onboard corporate directories.

---

## Standard B2B Account Payload

To onboard a corporate Account, post this exact JSON body to Liferay's headless administrative user endpoint:

```json
{
  "name": "Everflow Heavy Industries",
  "externalReferenceCode": "everflow-account-erc",
  "description": "B2B Manufacturer primary corporate account directory."
}
```

**Target Endpoint:** `/o/headless-admin-user/v1.0/accounts`
