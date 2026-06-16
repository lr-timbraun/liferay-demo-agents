# Calling Liferay APIs via FreeMarker (restClient)

In Liferay 7.4+, fragments can perform server-side API calls using the built-in **`restClient`** object. This is the preferred method for fetching data from Headless Delivery or Liferay Objects.

## Key Principles
- **Internal Dispatch:** It performs an internal servlet dispatch (no outbound HTTP request), making it fast and secure.
- **Permission Aware:** It automatically respects the permissions of the current user.
- **Return Type:** `restClient.get()` calls return raw JSON **Strings** rather than FreeMarker objects. You MUST parse the string before using it.
- **Alternative Syntax:** Fragments MUST use the square-bracket syntax (e.g., `[#assign ... /]`).

## Mandatory Parsing Pattern
Because the API returns a string, you must use `jsonFactoryUtil` to deserialize it defensively.

```html
[#-- 1. Fetch raw string --]
[#assign rawData = restClient.get("/o/c/myobjects/")!"" /]

[#-- 2. Defensive Parse --]
[#assign data = {"items": []} /]
[#if rawData?is_string && rawData?trim?starts_with("{")]
    [#attempt]
        [#assign data = jsonFactoryUtil.looseDeserialize(rawData) /]
    [#recover]
        [#-- Handle parse error --]
    [/#attempt]
[#elseif !rawData?is_string]
    [#-- Handle cases where it might already be an object in some contexts --]
    [#assign data = rawData /]
[/#if]

[#-- 3. Null-Safe Access --]
[#list data.items as item]
    ${(item.property)!"Default Value"}
[/#list]
```

## Common API Endpoints
- **Liferay Objects:** `/o/c/<object-plural-name>/`
- **Blogs:** `/o/headless-delivery/v1.0/sites/${groupId}/blog-entries`
- **Documents:** `/o/headless-delivery/v1.0/sites/${groupId}/documents`

## Implementation Examples

### 1. Fetching Object Data
To list items from a custom Object named `Partner`:

```html
[#assign rawPartners = restClient.get("/o/c/partners/")!"" /]
[#assign partners = {"items": []} /]

[#if rawPartners?is_string && rawPartners?trim?has_content]
    [#assign partners = jsonFactoryUtil.looseDeserialize(rawPartners) /]
[/#if]

<div class="partner-list">
    [#list partners.items as partner]
        <div class="partner-card">
            <h3>${(partner.name)!""}</h3>
            <p>${(partner.description)!""}</p>
        </div>
    [/#list]
</div>
```

## Important Notes
- **Null Safety:** Always use FreeMarker's default value operator (`!`) and parentheses for deep access: `${(item.parent.child.name)!''}`.
- **API Explorer:** Use `/o/api` on your Liferay instance to discover paths and schemas.
