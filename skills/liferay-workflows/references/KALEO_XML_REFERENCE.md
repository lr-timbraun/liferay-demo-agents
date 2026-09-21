# Guide: Liferay Kaleo XML Workflows

This reference guide provides the exact XML schema definition required to structure an approval process inside the Liferay Workflow Engine.

---

## Standard Kaleo XML Schema

Every XML workflow model file inside its assigned individual directory (e.g. `liferay/workflows/{workflow-name}/`) MUST validate against this exact layout pattern:

```xml
<?xml version="1.0"?>
<workflow-definition xmlns="urn:liferay.com:lz-workflow-definition:1.0">
    <name>Standard Approval</name>
    <state>
        <name>created</name>
        <transitions>
            <transition>
                <name>submit</name>
                <target>review</target>
            </transition>
        </transitions>
    </state>
</workflow-definition>
```
