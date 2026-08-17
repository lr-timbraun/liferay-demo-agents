---
name: generate-images
description: Workflow management for Imagen 4 / Gemini 3.1 Flash Image generation and post-processing. Use when generating AI assets, enforcing aspect ratios (e.g. 16:9), changing resolutions (1K or 2K), or optimizing file sizes for web delivery.
---

# Skill: Generate Images (Sub-Agent Implementation)

## Description
This skill provides implementation guidance for generating high-quality product assets, homepage heroes, and B2B media catalogs using the `gemini-3.1-flash-image` API model. It is designed to be executed by sub-agents to prepare pristine visual assets for Liferay projects.

## STRICT EXECUTION PROTOCOL (MANDATORY READS)

You MUST NOT attempt to write API calls to the model from memory. You MUST use the `read_file` tool to read the following reference document BEFORE generating images:

- **Gemini Flash Image API Usage**: You MUST read **[GEMINI_3_1_FLASH_IMAGE_GUIDE.md](references/GEMINI_3_1_FLASH_IMAGE_GUIDE.md)** to obtain the correct Python script templates, endpoint URLs, and valid parameter configurations (e.g., `aspectRatio`, `sampleImageSize`).

## Supplemental Guidance

### 1. Model Configuration
- **Model ID:** Always use the active `gemini-3.1-flash-image` model.
- **Endpoint Structure:** Run standard `generateContent` requests directly against the Google Generative Language v1beta REST API using the user's `GEMINI_API_KEY` (or fallback keys).

### 2. Implementation: Aspect Ratio & Size
- **Descriptive Prompt Hints:** Because native JSON properties can vary, always append aspect ratio and resolution preferences directly to the text prompt string (e.g., `"Aspect Ratio: 16:9, Size: 1K"`).
- **Resolution Cap:** Prefer generating `1K` over `2K` to ensure optimal performance, low latency, and rapid image processing on target local systems.

### 3. Image Post-Processing (Pillow)
- **Web-Ready Compression:** After generating images, use Python's standard `Pillow` library to resize and compress large PNG payloads to highly optimized, compact JPEGs before uploading to Liferay, reducing bandwidth congestion.

## Available Resources
- Liferay Learn - Documents and Media APIs: https://learn.liferay.com/w/dxp/content-authoring-and-management/documents-and-media/developer-guide/apis
- Reference: Gemini 3.1 Flash Image Guide: `references/GEMINI_3_1_FLASH_IMAGE_GUIDE.md`
