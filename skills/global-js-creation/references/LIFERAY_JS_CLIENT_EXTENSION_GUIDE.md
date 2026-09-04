# Guide: Liferay JS Client Extensions

This reference guide provides the exact YAML structure required to declare a standard global JS client extension in Liferay DXP.

---

## Standard Descriptor Schema

Every JS client extension folder MUST contain a `client-extension.yaml` file conforming to this exact structure:

```yaml
custom-global-js:
    name: Custom Global JS
    type: globalJS
    urls:
        - custom.js
```

The compiled output will automatically be packaged into a LUFFA ZIP archive by Liferay's native Gradle build scripts during Phase 2 hot-deployments.
