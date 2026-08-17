# Liferay Commerce Catalog and Taxonomy Guide

This guide details the structures and API workflows required to programmatically define B2B Commerce catalogs, taxonomies (vocabularies and categories), and product specification fields inside a Liferay Workspace.

---

## 1. Creating Taxonomies (Vocabularies and Categories)

Before products are injected, you must define the category classifications (taxonomies) used by buyers to browse and filter the storefront.

All taxonomies must be created using Liferay's standard Headless Admin Taxonomy REST endpoints.

### A. Create a Taxonomy Vocabulary
*   **Endpoint:** `POST /o/headless-admin-taxonomy/v1.0/taxonomy-vocabularies`
*   **Payload:**
    ```json
    {
        "name": {"en_US": "Therapeutic Areas"},
        "externalReferenceCode": "therapeutic-areas-vocabulary"
    }
    ```

### B. Create Taxonomy Categories
*   **Endpoint:** `POST /o/headless-admin-taxonomy/v1.0/taxonomy-vocabularies/{vocabularyId}/taxonomy-categories`
*   **Payload:**
    ```json
    {
        "name": {"en_US": "Cardiovascular"},
        "externalReferenceCode": "category-cardiovascular"
    }
    ```

---

## 2. Catalog Management

Products in Liferay Commerce reside inside a **Catalog**. When building populator scripts, you should never hardcode the `catalogId`. Instead, query Liferay to dynamically resolve the catalog ID or read it from LDM's meta context.

*   **Endpoint to List Catalogs:** `GET /o/headless-commerce-admin-catalog/v1.0/catalogs`

---

## 3. Product Specification Fields

Product Specifications (like "Active Ingredient" or "Strength") are global, prerequisite properties. They are defined once globally and then attached to specific products with localized values.

When creating specifications via scripts, **always set `"facetable": true`** in the payload. This ensures that Liferay automatically generates faceted navigation filters for these specifications in the store search sidebar.

### Create Global Specification Field
*   **Endpoint:** `POST /o/headless-commerce-admin-catalog/v1.0/specifications`
*   **Payload:**
    ```json
    {
        "key": "dosage-strength",
        "title": {"en_US": "Dosage Strength"},
        "facetable": true
    }
    ```
