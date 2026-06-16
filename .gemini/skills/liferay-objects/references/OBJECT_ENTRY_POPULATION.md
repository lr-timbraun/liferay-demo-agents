# Guide: Populating Liferay Object Entries

This guide provides the implementation patterns for programmatically generating and submitting demo data entries to published Liferay Objects.

## Core API Details
- **Endpoint:** `POST /o/c/{objectPluralName}/`
- **Auth:** Basic Auth (using credentials from `.env`).

## Implementation Pattern (Python)

```python
import os
import requests
import json

# Setup from .env
email = os.environ.get("LIFERAY_ADMIN_EMAIL_ADDRESS")
password = os.environ.get("LIFERAY_ADMIN_PASSWORD")
host = "https://webserver-{reponame}-prd.lfr.cloud"

def create_entry(plural_name, entry_data):
    url = f"{host}/o/c/{plural_name}/"
    response = requests.post(url, auth=(email, password), json=entry_data)
    return response.json()
```

## Mandatory Standards
- **Industry Relevance:** Data MUST be directly related to the prospect's industry (e.g., "Healthcare Patient Records" for a hospital).
- **No Placeholders:** Avoid "test", "lorem ipsum", or "123". Use realistic names, dates, and descriptions.
- **Narrative Alignment:** Ensure the data supports the story defined in the `DEMO_PLAN.md`.
- **Relational Integrity:** When linking entries, use the `r_{relationshipName}_{relatedObject}Id` format and provide the exact integer ID of the related entity.

## Data Generation Tips
- Use Python's `random` or `faker` (if available) to create variability.
- Always include a unique `externalReferenceCode` for every entry to allow for idempotent updates.
- Format dates according to ISO 8601 (e.g., `2025-12-16T14:30:00Z`).
