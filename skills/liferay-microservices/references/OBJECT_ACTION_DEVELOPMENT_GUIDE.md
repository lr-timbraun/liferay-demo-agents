# Guide: Liferay Object Action Handlers (REST)

This reference guide details how to build secure backend microservice endpoints capable of handling Liferay Object Actions.

---

## Standard JSON Payload Schema

When an Object event triggers, Liferay DXP posts this exact JSON body structure to your microservice:

```json
{
  "objectEntryId": 12345,
  "objectDefinitionKey": "C_SupportTicket",
  "values": {
    "title": "Hardware issue",
    "description": "The laptop does not boot."
  }
}
```
Your backend route must parse this structure, perform validation, and return an appropriate HTTP status code (such as `200` for OK, or `400` with an error message to block submission).
