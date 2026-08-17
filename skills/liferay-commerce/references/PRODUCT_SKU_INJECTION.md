# B2B Product and SKU Injection Guide

This guide details the sequential API workflow required to programmatically inject B2B products, link specification values, define global option templates, and map variant SKUs and price structures.

---

## The External Reference Code (ERC) Mandate

**CRITICAL RULE:** In Liferay DXP Commerce, internal integer IDs (`id`) of newly created products can be highly unstable across deployments. For all subsequent updates, category mappings, and image attachments, you MUST strictly use the External Reference Code (ERC) endpoints.

*   **REST Path Pattern:** `/products/by-externalReferenceCode/{ERC}`

---

## Step-by-Step Product Lifecycle Workflow

Follow this exact sequence to ensure B2B products compile and deploy without relational integrity breaks.

### Step 1: Create Product (Standard Simple Product)
Generate the base product wrapper. You MUST provide a unique, uppercase string for the `externalReferenceCode` during this initial post.

*   **Endpoint:** `POST /o/headless-commerce-admin-catalog/v1.0/products`
*   **Payload:**
    ```json
    {
        "active": true,
        "catalogId": 12345,
        "externalReferenceCode": "PRODUCT-MED-100",
        "name": {"en_US": "Atorvastatin 20mg Tablets"},
        "productType": "simple"
    }
    ```

### Step 2: Assign Taxonomy Categories
Associate the product with one or more pre-created categories using the ERC path.

*   **Endpoint:** `PATCH /o/headless-commerce-admin-catalog/v1.0/products/by-externalReferenceCode/{ERC}/categories`
*   **Payload:**
    ```json
    [
        {"id": 99991}
    ]
    ```

### Step 3: Attach Option Templates
Options (like variant pack sizes or dosages) are **global, prerequisite entities**. They are NOT created within the product. You must create the option once globally, and then link it to your product using its option ID.

*   **Create Option Globally:** `POST /o/headless-commerce-admin-catalog/v1.0/options`
*   **Attach Option to Product via ERC:** `PATCH /o/headless-commerce-admin-catalog/v1.0/products/by-externalReferenceCode/{ERC}`
*   **Payload:**
    ```json
    {
        "productOptions": [
            {
                "optionId": 88881,
                "fieldType": "select",
                "required": true
            }
        ]
    }
    ```

### Step 4: Map Variant SKUs
If a product has options, you MUST define distinct, variant SKU entries (mapping pricing, publish states, and option value links) to allow buyers to purchase specific combinations.

*   **Endpoint:** `POST /o/headless-commerce-admin-catalog/v1.0/products/by-externalReferenceCode/{ERC}/skus`
*   **Payload:**
    ```json
    {
        "sku": "SKU-MED-100-PACK28",
        "price": 45.0,
        "purchasable": true,
        "published": true,
        "skuOptions": [
            {
                "optionId": 88881,
                "optionValueId": 88882
            }
        ]
    }
    ```

### Step 5: Map Product Specifications
To attach specifications, do NOT use nested POST sub-resource endpoints (which are highly unstable). Instead, use the global product ERC PATCH endpoint and supply a localized specifications array.

*   **Endpoint:** `PATCH /o/headless-commerce-admin-catalog/v1.0/products/by-externalReferenceCode/{ERC}`
*   **Payload:**
    ```json
    {
        "productSpecifications": [
            {
                "specificationKey": "dosage-strength",
                "value": {"en_US": "20 mg"}
            }
        ]
    }
    ```
