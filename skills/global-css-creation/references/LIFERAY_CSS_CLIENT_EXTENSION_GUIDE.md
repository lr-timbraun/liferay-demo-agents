# Guide: Liferay CSS Client Extensions

This reference guide provides the exact YAML structure required to declare a standard global CSS client extension in Liferay DXP.

---

## Standard Descriptor Schema

Every CSS client extension folder MUST contain a `client-extension.yaml` file conforming to this exact structure:

```yaml
custom-global-css:
    name: Custom Global CSS
    type: globalCSS
    urls:
        - custom.css
```

The compiled output will automatically be packaged into a LUFFA ZIP archive by Liferay's native Gradle build scripts during Phase 2 hot-deployments.
