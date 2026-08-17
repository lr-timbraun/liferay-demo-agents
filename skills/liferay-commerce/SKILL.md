---
name: liferay-commerce
description: Implementation guidance for programmatically creating B2B commerce catalogs, products, options, variant SKUs, and specifications.
---

# Skill: Liferay Commerce (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for programmatically creating high-impact B2B commerce catalogs, options, variant SKUs, specifications, and categories. It is designed to be executed by the commerce-agent using an intent-based specification.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to build Liferay Commerce setups from memory. You MUST use the `read_file` tool to read the following reference documents BEFORE generating any code or executing any Python data-population scripts:

- **Catalog & Taxonomy**: Read **[CATALOG_TAXONOMY_GUIDE.md](references/CATALOG_TAXONOMY_GUIDE.md)** to configure taxonomies, vocabularies, categories, and set `"facetable": true` specification fields.
- **Product & SKU Injection**: Read **[PRODUCT_SKU_INJECTION.md](references/PRODUCT_SKU_INJECTION.md)** to adhere to the External Reference Code (ERC) mandate, attach global option templates, and link purchasable variant SKUs.
- **Asset & Copy Pipeline**: Read **[COMMERCE_ASSET_PIPELINE.md](references/COMMERCE_ASSET_PIPELINE.md)** to generate LLM product copy, compress generated images locally using Pillow, and attach Base64 images with `"neverExpire": true`.

## Supplemental Guidance

### 1. Spec Ingestion
- **Read the Spec:** Locate and read the provided technical specification (e.g., `specs/objects/commerce-catalog.md`).
- **Analyze Intent:** Identify the required catalog name, taxonomy (vocabularies and categories), and the specific product option templates and variant SKUs needed.

### 2. Implementation: Project Structure & Boilerplates
- **Location:** Place any generated Python populator scripts inside the assigned directory relative to the workspace root (e.g. `scripts/populate-catalog.py`).
- **Pristine Boilerplate:** Always structure your Python requests utilizing the "Gold Standard Boilerplate Script" detailed inside the reference guide. Never copy legacy scripts that contain outdated nested POST patterns.

### 3. Image Optimization Mandate
- **Resizing:** You MUST use the Python `Pillow` library to resize and compress any generated high-resolution product images locally before uploading to conserve bandwidth.
- **Never Expire:** When attaching Base64 images to products, you MUST pass `"neverExpire": true` in the JSON payload to ensure images remain active and loaded throughout the demo lifecycle.

## Available Resources
- Liferay Learn - Liferay Commerce APIs: https://learn.liferay.com/w/dxp/commerce/developer-guide/apis
- Reference: Catalog and Taxonomy: `references/CATALOG_TAXONOMY_GUIDE.md`
- Reference: Product and SKU Injection: `references/PRODUCT_SKU_INJECTION.md`
- Reference: Asset and Copy Pipeline: `references/COMMERCE_ASSET_PIPELINE.md`
