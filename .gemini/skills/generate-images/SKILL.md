---
name: generate-images
description: Workflow management for Imagen 4 image generation and post-processing. Use when generating AI assets, enforcing aspect ratios (e.g. 16:9), changing resolutions (1K or 2K), or optimizing file sizes for web delivery.
---

# Skill: Generate Images

## Description
This skill provides implementation guidance for using the `imagen-4.0-generate-001` model to generate and process visual assets for Liferay projects.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write API calls to the Imagen 4 model from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating images:

- **Imagen API Usage**: Read **[IMAGEN_4_GUIDE.md](references/IMAGEN_4_GUIDE.md)** to obtain the correct Python script templates, endpoint URLs, and valid parameter configurations.

## Supplemental Guidance

### 1. Implementation: Image Generation
- **descriptive Prompts:** Use the Imagen 4 model via Python REST API calls.
- **Aspect Ratio:** Use the API's `aspectRatio` parameter natively or use Python (Pillow) to crop generated images.
- **Resolution:** Change resolution sizes using the `sampleImageSize` parameter (prefer `1K` over `2K`).

### 2. Implementation: Post-Processing
- **Format Optimization:** Convert large PNG assets to compressed JPEGs or WebP for better web performance.
- **Icon & Pattern Generation:** Follow specialized instructions for UI elements and tiling backgrounds in the reference guide.

## Validation Phase
- **Quality Check:** Verify text accuracy and stylistic consistency in generated assets.
- **Optimization:** Confirm that file sizes are optimized for web delivery.

## Available Resources
- Reference: Imagen API Usage: `references/IMAGEN_4_GUIDE.md`
