---
name: liferay-microservices
description: Guidelines for packaging Python or Node.js backend client extensions (REST providers) to handle Liferay Object Actions and Workflow Actions.
---

# Skill: Liferay Microservices (REST Providers)

## Description
This skill provides implementation guidelines, routes, and schemas for packaging lightweight Python or Node.js backend services configured as Client Extensions to securely handle Object and Workflow events.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to construct microservice routes from memory. You MUST load and read these files BEFORE executing backend creation tasks:
- **Object Action Development Guide**: Read **[references/OBJECT_ACTION_DEVELOPMENT_GUIDE.md](references/OBJECT_ACTION_DEVELOPMENT_GUIDE.md)** to obtain the HTTP Post payload schemas.
- **Workflow Action Development Guide**: Read **[references/WORKFLOW_ACTION_DEVELOPMENT_GUIDE.md](references/WORKFLOW_ACTION_DEVELOPMENT_GUIDE.md)** to obtain the workflow transition parameters.

## Available Resources
- Object Action Guide: `references/OBJECT_ACTION_DEVELOPMENT_GUIDE.md`
- Workflow Action Guide: `references/WORKFLOW_ACTION_DEVELOPMENT_GUIDE.md`
- Python Boilerplate App: `templates/python-microservice/app.py`
- Descriptor Template: `templates/python-microservice/client-extension.yaml`
- Requirements: `templates/python-microservice/requirements.txt`
