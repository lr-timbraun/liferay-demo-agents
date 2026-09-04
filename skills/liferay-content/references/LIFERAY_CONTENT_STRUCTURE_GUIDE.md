# Guide: Liferay Web Content Structures (JSON)

This reference guide provides the standard JSON schema layout required to define Liferay Web Content Structures.

---

## Standard JSON Schema Definition

Every web content structure file inside `liferay/content/structures/` MUST conform to this exact JSON schema:

```json
{
  "fields": [
    {
      "label": "Title",
      "name": "title",
      "type": "text",
      "required": true
    },
    {
      "label": "Body Copy",
      "name": "body",
      "type": "html",
      "required": false
    }
  ]
}
```
