# Guide: Liferay Workflow Action Handlers (REST)

This reference guide details how to build secure backend microservice endpoints capable of handling Liferay Workflow Action transitions.

---

## Standard Callback Sequence

When a workflow transition task triggers, Liferay's workflow engine posts the transaction payload containing the transition parameters to your microservice:

```json
{
  "workflowInstanceId": 54321,
  "transitionName": "approve",
  "comment": "Verified and approved by backend system."
}
```
Your microservice must authenticate using standard OAuth2 headless client-extension configurations and callback safely to finalize the transition state inside DXP.
