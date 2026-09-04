# Guide: Token Mapping Standards for Stylebooks

This reference document defines Liferay's standard Classic theme token mapping schema.

---

## Standard Token Variables Map

Every `frontend-tokens-values.json` file inside `liferay/stylebooks/` MUST map the Brand guidelines into these exact semantic Liferay tokens:

```json
{
  "colors": {
    "primary": "#0056B3",
    "secondary": "#6C757D",
    "success": "#28A745",
    "info": "#17A2B8",
    "warning": "#FFC107",
    "danger": "#DC3545",
    "light": "#F8F9FA",
    "dark": "#343A40"
  },
  "font-size": {
    "base": "1rem",
    "h1": "2.5rem",
    "h2": "2rem",
    "h3": "1.75rem",
    "h4": "1.5rem"
  },
  "border-radius": {
    "base": "0.25rem",
    "large": "0.3rem",
    "small": "0.2rem"
  }
}
```

Ensure color values are written as uppercase HEX string variables to prevent CSS parser mismatches inside Liferay DXP.
