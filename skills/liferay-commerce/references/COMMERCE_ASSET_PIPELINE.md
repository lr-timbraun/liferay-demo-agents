# Liferay Commerce Asset and Copywriting Pipeline

This guide details the copy generation standards and local Python image-optimization workflows required to prepare and upload high-impact visual assets to Liferay Commerce.

---

## 1. AI-Driven Copywriting Standards

Demo catalogs should look completely realistic. You MUST use an LLM (such as Gemini 2.5 Flash) to dynamically generate high-quality product descriptions tailored to the prospect's industry.

*   **`shortDescription`**: Must be a punchy marketing summary of around 50 words, formatted as plain text.
*   **`description`**: Must be a detailed, professional B2B product description of around 500 words, focusing on enterprise benefits, technical capabilities, or pharmaceutical features, formatted in basic HTML elements (`<p>`, `<ul>`, `<li>`, `<strong>`).

---

## 2. The Three-Image Solution

To present a highly polished B2B catalog, you should generate and link exactly **three distinct, high-quality images** for every product:

1.  **Priority 0 (Primary Visual):** Clean packaging mock-up.
2.  **Priority 1:** Clean, high-resolution product shot.
3.  **Priority 2:** Contextual usage shot (e.g. medical consultation, clinical setup).

---

## 3. Local Python Image Optimization

High-resolution generated assets can be huge. Before uploading, you MUST use Python's **Pillow** library to automatically resize and compress images locally, preventing container timeouts and preserving memory.

### Boilerplate Optimization Routine:
```python
import io
import base64
from PIL import Image

def optimize_and_encode_image(image_path, max_size=(800, 800), quality=85):
    """Resizes and compresses an image locally, returning its Base64 string."""
    with Image.open(image_path) as img:
        # Convert RGBA to RGB to support JPEG compression
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Resize maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save compressed bytes in memory
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", quality=quality)
        
        # Encode to base64
        byte_data = output_buffer.getvalue()
        return base64.b64encode(byte_data).decode('utf-8')
```

---

## 4. Base64 Upload to Product ERC

Once your Base64 string is ready, upload it directly using the product's External Reference Code (ERC) endpoint.

### Crucial Security Parameter
You MUST set **`"neverExpire": true`** in your JSON payload. If omitted, Liferay DXP may expire the attachment, causing images to disappear from your storefront over time.

*   **Endpoint:** `POST /o/headless-commerce-admin-catalog/v1.0/products/by-externalReferenceCode/{ERC}/images/by-base64`
*   **Payload:**
    ```json
    {
        "attachment": "BASE64_ENCODED_STRING_OF_OPTIMIZED_IMAGE",
        "contentType": "image/jpeg",
        "priority": 0,
        "title": {"en_US": "Main Packaging Image"},
        "neverExpire": true
    }
    ```
