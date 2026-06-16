# Guide: Liferay Classic Theme Token Mapping

This guide ensures consistent and correct usage of Liferay's Classic theme CSS variables in Stylebooks and Client Extensions.

## Understanding the Token Source
The master list of tokens is found in [frontend-token-definition.json](https://github.com/liferay/liferay-portal/blob/master/modules/apps/frontend-theme/frontend-theme-classic/src/WEB-INF/frontend-token-definition.json).

### JSON Structure Anatomy
Each token in the definition file follows this pattern:
```json
{
    "id": "brand-color-1",
    "label": "brand-color-1",
    "mappings": [
        {
            "type": "css-variable",
            "value": "brand-color-1"
        }
    ],
    "type": "color"
}
```
**CRITICAL:** The CSS variable you use in your code (`var(--brand-color-1)`) and in the `frontend-tokens-values.json` (`cssVariableMapping`) MUST match the string found in the `mappings/value` field of the source JSON.

## Mapping Logic (Semantic Priority)
Always map brand assets to the most semantically relevant token.

### 1. Color Mapping
- **Primary Brand Identity:** Use `brand-color-1` through `brand-color-4` (Note: Only 4 brand slots exist).
- **UI Actions:** Use `primary` (main buttons/links), `secondary`, `success`, `info`, `warning`, `danger`.
- **Neutrals:** Use `gray-100` (lightest) through `gray-900` (darkest).

### 2. Typography Mapping
- **Families:** Use `font-family-base`, `font-family-monospace`, or `font-family-sans-serif`.
- **Weights:** Use `font-weight-light`, `font-weight-normal`, `font-weight-semi-bold`, `font-weight-bold`.
- **Sizes:** Use `font-size-base`, `font-size-sm`, or heading tokens (`h1-font-size`, etc.).

### 3. Component-Level Mapping (Strategic Usage)
Override Liferay's default style ONLY for elements that are relevant to the demo. Use the VERIFIED names below:
- **Primary Buttons:** `btn-primary-background-color`, `btn-primary-border-color`, `btn-primary-color`.
- **Primary Button Hover:** `btn-primary-hover-background-color`, `btn-primary-hover-border-color`, `btn-primary-hover-color`.
- **Secondary Buttons:** `btn-secondary-background-color`, `btn-secondary-border-color`, `btn-secondary-color`.
- **Secondary Button Hover:** `btn-secondary-hover-background-color`, `btn-secondary-hover-border-color`, `btn-secondary-hover-color`.
- **General UI:** `body-bg`, `body-color`, `border-radius`, `box-shadow`.

## Verification Checklist
1. **Source Check:** Does the variable name exist in the `mappings/value` field of the official `frontend-token-definition.json`?
2. **Type Check:** Is the token type appropriate for the value?
3. **Relevance Check:** Have you focused your effort on the components that matter most for the demo's narrative?
4. **Usage Check:** Are you using `var(--token-name)` in your CSS?
