# Liferay Form Fragment Development Guide

This guide outlines the mandatory requirements for creating fragments that can be used within Liferay Form Containers to submit data to Liferay Objects.

## Mandatory `fragment.json` Configuration
*   **Type:** The `type` property MUST be set to `"form-fragment"`.
*   **Field Types:** You must define which Object field types this fragment supports in the `fieldTypes` array.
    *   **Valid Strings:** `text`, `string`, `number`, `integer`, `decimal`, `date`, `date-time`, `boolean`, `rich-text`, `multiselect`.
    *   **Example:** `"fieldTypes": ["text", "string", "rich-text"]`

## HTML Structure & Binding
Form fragments rely on the global `${input}` variable provided by the Form Container. You MUST bind HTML attributes to this variable for mapping to function.

### 1. Mandatory Input Name
The `name` attribute of your HTML input/select/textarea element MUST be set to the system-provided name:
```html
<input name="${input.name}" ... />
```

### 2. Value and Required Binding
Bind the `value` and `required` states to the Object field configuration:
```html
<input 
    name="${input.name}" 
    value="${input.value!''}" 
    [#if input.required]required[/#if]
    ... 
/>
```

### 3. Labels and Validation
Use the `${input.label}` for the field label and `${input.errorMessage}` to display validation errors:
```html
<label>${input.label}</label>
<div class="error-message">${input.errorMessage!''}</div>
```

## The `${input}` Variable Reference
- `input.name`: (String) The internal name required for the `name` attribute.
- `input.label`: (String) The user-friendly label for the field.
- `input.value`: (Any) The current value of the field.
- `input.required`: (Boolean) Whether the field is mandatory.
- `input.errorMessage`: (String) Contains any validation error messages.
- `input.attributes`: (Map) Contains type-specific metadata (e.g., `options` for selects).
