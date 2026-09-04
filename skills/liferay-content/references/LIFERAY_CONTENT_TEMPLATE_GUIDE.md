# Guide: Liferay Web Content FreeMarker Templates

This reference guide provides standard FreeMarker variables and display tags to render structured web content inside Liferay DXP.

---

## Standard FreeMarker Syntax

Every FreeMarker FTL file inside `liferay/content/templates/` MUST use standard server-side expression tags:

```ftl
<div class="content-template">
    <h2>${title.getData()}</h2>
    <div class="content-body">
        ${body.getData()}
    </div>
</div>
```
