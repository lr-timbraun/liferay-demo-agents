# Liferay Page Creation and Page Templates Guide

This guide details the standard paths, locator patterns, and Playwright-based UI automation flows required to programmatically or interactively create Liferay Master Pages, Content Page Templates, and regular Content Pages inside a Site.

---

## 1. Master Pages Management

Master Pages define the global header, footer, and sidebars that remain consistent across multiple pages.

### A. Navigation URL
Administer Master Page Templates by navigating to the layout templates portlet under your target site's control panel:
`{LIFERAY_HOST}/group/{siteFriendlyUrl}/~/control_panel/manage/-/layout_page_template_admin_web/master_layouts`

### B. Playwright UI Automation Pattern
```javascript
// Navigate to Master Pages administration
const masterPageUrl = `${host}/group/${siteFriendlyUrl}/~/control_panel/manage/-/layout_page_template_admin_web/master_layouts`;
await page.goto(masterPageUrl);

// Click "Add" button to create a new Master Page Template
await page.click('button[aria-label="Add"], .btn-add');
await page.fill('input[name="name"]', 'Brand Master Page');
await page.click('button[type="submit"], .btn-save');

// Wait for the Page Editor iframe/container to load
await page.waitForSelector('.page-editor-container');
```

---

## 2. Content Page Templates

Content Page Templates (or Page Templates) define reusable page layout blueprints (with pre-placed fragments and widgets) that editors can select when creating new content pages.

### A. Navigation URL
Administer Content Page Templates by navigating to the layout templates portlet under your target site's control panel:
`{LIFERAY_HOST}/group/{siteFriendlyUrl}/~/control_panel/manage/-/layout_page_template_admin_web/page_templates`

### B. Playwright UI Automation Pattern
```javascript
// Navigate to Content Page Templates administration
const pageTemplateUrl = `${host}/group/${siteFriendlyUrl}/~/control_panel/manage/-/layout_page_template_admin_web/page_templates`;
await page.goto(pageTemplateUrl);

// Create a Page Template Collection / Set first (if it doesn't exist)
await page.click('button[aria-label="Add Collection"], .btn-add-collection');
await page.fill('input[name="name"]', 'Wholesale Storefront Templates');
await page.click('button[type="submit"]');

// Open the newly created collection and click "Add" to create a template
await page.click('.collection-card-title:has-text("Wholesale Storefront Templates")');
await page.click('button[aria-label="Add Template"], .btn-add-template');
await page.fill('input[name="name"]', 'Product Detail Template');
await page.click('button[type="submit"]');

// Wait for the Page Editor workspace to initialize
await page.waitForSelector('.page-editor-workspace');
```

---

## 3. Regular Content Pages

Content Pages are standard, interactive pages inside a Liferay Site. They are built by dragging, dropping, and configuring Page Fragments directly onto the page layout.

### A. Navigation URL
Administer and create regular Site Pages by navigating to the Page Layout administration portlet:
`{LIFERAY_HOST}/group/{siteFriendlyUrl}/~/control_panel/manage/-/layout/pages`

### B. Playwright UI Automation Pattern
```javascript
// Navigate to Pages administration
const pagesAdminUrl = `${host}/group/${siteFriendlyUrl}/~/control_panel/manage/-/layout/pages`;
await page.goto(pagesAdminUrl);

// Click "Add" and select "Public Page" or "Private Page"
await page.click('button[aria-label="Add Page"], .btn-add-page');
await page.click('.dropdown-item:has-text("Public Page")');

// Select page type (blank Content Page or select from Page Templates Collection)
await page.click('.page-type-card:has-text("Content Page")');
await page.fill('input[name="name"]', 'Partner Storefront');
await page.click('button[type="submit"]');

// Wait for the newly created page to load in Page Editor mode
await page.waitForSelector('.page-editor-container');
```

---

## 4. Key Visual Page Editor Controls (Playwright)

When editing Master Pages, Page Templates, or Content Pages, use these standard Liferay editor selectors to interact with fragments, configure editable fields, and publish changes:

1.  **Open Sidebar / Fragments Panel:**
    `await page.click('button[aria-label="Add Elements"], .sidebar-control-add');`
2.  **Search and Drag Fragment:**
    ```javascript
    // Search for your custom fragment
    await page.fill('input[placeholder="Search"], .fragments-search-input', 'My Custom Hero');
    // Locate the draggable fragment card
    const draggable = page.locator('.fragment-card:has-text("My Custom Hero")');
    // Locate the drop zone container on the page
    const dropzone = page.locator('.page-editor-drop-zone, .lfr-layout-structure-item');
    // Perform the drag and drop operation
    await draggable.dragTo(dropzone);
    ```
3.  **Publish Page Changes:**
    `await page.click('button:has-text("Publish"), .btn-publish');`
