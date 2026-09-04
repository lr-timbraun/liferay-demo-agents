---
name: product-creation
description: Injecting B2B product records, option templates, and multi-value variant SKUs via Headless APIs.
---

# Skill: Product Creation (SKU Injections)

## Description
This skill provides guidelines and JSON payload schemas for injecting B2B products, option templates, and multi-value variant SKUs via Liferay Commerce Headless APIs.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to inject product SKUs from memory. You MUST load and read these files BEFORE executing product creation tasks:
- **Product SKU Injection Guide**: Read **[references/PRODUCT_SKU_INJECTION.md](references/PRODUCT_SKU_INJECTION.md)** to obtain the exact variant and SKU payload structures.

## Available Resources
- Product SKU Injection Guide: `references/PRODUCT_SKU_INJECTION.md`
