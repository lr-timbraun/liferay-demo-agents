# Guide: Commerce Product SKU Injection (Headless)

This reference guide details standard JSON payload structures required to create multi-value variant products in Liferay Commerce.

---

## Standard Product SKU Payload

Every product injection request MUST conform to this exact JSON body:

```json
{
  "productType": "simple",
  "name": {
    "en_US": "Premium Hydraulic Valve"
  },
  "sku": "VALVE-PREM-01",
  "active": true,
  "prices": [
    {
      "priceListKey": "standard-prices-erc",
      "price": 249.99
    }
  ]
}
```
