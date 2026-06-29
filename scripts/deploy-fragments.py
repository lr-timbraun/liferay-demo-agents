#!/usr/bin/env python3
import os
import sys
import zipfile
import tempfile
from playwright.sync_api import sync_playwright

# Import standard credential utility
sys.path.append(os.path.dirname(__file__))
import env_utils

def get_fragments_dir():
    """Locates the liferay/fragments folder in the workspace."""
    cwd = os.getcwd()
    fragments_path = os.path.join(cwd, 'liferay', 'fragments')
    if os.path.exists(fragments_path):
        return fragments_path
    return None

def package_fragments(collection_dir, output_zip):
    """
    Packages a Liferay Fragment Collection into a ZIP file.
    Follows the strict structure expected by Liferay's importer.
    """
    collection_root_name = os.path.basename(collection_dir.rstrip('/\\'))
    
    # Check for collection metadata
    if not os.path.exists(os.path.join(collection_dir, 'collection.json')):
        print(f"Error: Mandatory 'collection.json' missing in {collection_dir}")
        return False
        
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(collection_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # The arcname (path inside the ZIP) MUST start with the collection folder name
                relative_path = os.path.relpath(file_path, collection_dir)
                arcname = os.path.join(collection_root_name, relative_path)
                zipf.write(file_path, arcname=arcname)
    return True

def automate_ui_import(host, email, password, zipped_files):
    """Uses Playwright to log in and import packaged Fragment ZIP files into the Liferay Global Site."""
    print("\n--- Initiating Playwright Browser Automation ---")
    
    with sync_playwright() as p:
        # Launch Chromium headlessly
        print("Launching headless Chromium browser...")
        browser = p.chromium.launch(headless=True)
        
        # Create standard browser context (No SSL verification bypass to adhere to strict validation)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Login to Liferay
        login_url = f"{host}/c/portal/login"
        print(f"Navigating to login page: {login_url}...")
        page.goto(login_url)
        page.wait_for_load_state("networkidle")
        
        # Check if we are on the login form (using exact, language-independent element IDs)
        login_input = page.locator('#_com_liferay_login_web_portlet_LoginPortlet_login').first
        if login_input.count() > 0:
            print(f"Logging in as agent: {email}...")
            login_input.fill(email)
            
            password_input = page.locator('#_com_liferay_login_web_portlet_LoginPortlet_password').first
            password_input.fill(password)
            
            # Click Sign In (Using verified language-independent ID-based submit button)
            submit_btn = page.locator('button[id*="LoginPortlet_"][type="submit"]').first
            submit_btn.click()
            
            # Wait for Liferay's core theme marker indicating successful authentication on the body tag
            page.wait_for_selector('body.signed-in', timeout=20000)
            print("Login authenticated successfully!")
            
        page.wait_for_load_state("networkidle")
            
        # 2. Navigate to Global site Page Fragments Portlet
        fragments_url = f"{host}/group/global/~/control_panel/manage/-/fragments/fragment_collections"
        print(f"Navigating to Global Site Page Fragments Control Panel: {fragments_url}...")
        page.goto(fragments_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000) # Wait for list React component to render
        
        # 3. For each packaged collection, trigger the import
        for zip_path in zipped_files:
            collection_name = os.path.basename(zip_path).replace('.zip', '')
            print(f"\n[{collection_name}] Attempting to import {zip_path} via UI...")
            
            # Find and click the Actions / Options button in the management bar (Using the robust, nesting-resilient CSS selector based on title)
            actions_btn = page.locator('#portlet_com_liferay_fragment_web_portlet_FragmentPortlet button[title*="Fragment Sets Options"], #portlet_com_liferay_fragment_web_portlet_FragmentPortlet button[title="Fragment Sets Options"]').first
            if actions_btn.count() == 0:
                print(f"Error: Could not locate Actions/Dropdown menu on Page Fragments page. Saving screenshot.")
                page.screenshot(path="test-projects/import-error-actions.png")
                return False
                
            actions_btn.click()
            page.wait_for_timeout(500) # Let dropdown slide open
            
            # Click "Import" menuitem (strictly href/ID/attribute-based, supporting any language)
            import_menu_item = page.locator('.dropdown-menu a.dropdown-item[icon="import"], .dropdown-menu a[href*="view_import"]').first
            if import_menu_item.count() == 0:
                print(f"Error: Could not find 'Import' option in Actions dropdown. Saving screenshot.")
                page.screenshot(path="test-projects/import-error-menu.png")
                return False
                
            import_menu_item.click()
            print(f"[{collection_name}] Navigating to Import Collection sub-page...")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500) # Let the sub-page elements render
            
            # Set the ZIP file in Liferay's page file input (Strictly type/tag-based directly on the page)
            file_input = page.locator('input[type="file"]').first
            if file_input.count() == 0:
                print(f"Error: Could not find file input element on import sub-page. Saving screenshot.")
                page.screenshot(path="test-projects/import-error-fileinput.png")
                return False
                
            # Set local zip path
            file_input.set_input_files(zip_path)
            print(f"[{collection_name}] File uploaded to page.")
            
            # Click the primary "Import" button located in the top right corner of the .tbar (strictly Clay-based, no text)
            import_btn = page.locator('.tbar button.btn-primary, .tbar .btn-primary').first
            if import_btn.count() == 0:
                print(f"Error: Could not find primary Import button inside top right toolbar (.tbar). Saving screenshot.")
                page.screenshot(path="test-projects/import-error-submit.png")
                return False
                
            import_btn.click()
            print(f"[{collection_name}] Clicked import. Waiting for Liferay processing...")
            
            # 4. Handle \"Manage Existing Items\" modal if it appears (Duplication Conflict)
            try:
                # Wait up to 5 seconds to see if the \"Manage Existing Items\" modal opens
                print(f"[{collection_name}] Monitoring if 'Manage Existing Items' conflict dialog appears...")
                modal_selector = '.modal-dialog:has-text("Manage Existing Items"), .modal-dialog:has(input[value="overwrite"])'
                page.wait_for_selector(modal_selector, timeout=5000)
                
                print(f"[{collection_name}] Conflict detected! Selecting 'Overwrite Existing Items'...")
                # Select the radio button with value=\"overwrite\" inside the modal dialog
                overwrite_radio = page.locator('.modal-dialog input[type="radio"][value="overwrite"]').first
                overwrite_radio.click()
                
                # Click the \"Save\" primary button in the modal footer
                save_btn = page.locator('.modal-dialog .modal-footer button.btn-primary, .modal-dialog .modal-footer .btn-primary').first
                save_btn.click()
                print(f"[{collection_name}] Conflict resolved. Overwrite submitted!")
                
            except Exception:
                # If timeout occurs, it means there was no duplication conflict (imported directly!). We proceed gracefully.
                print(f"[{collection_name}] No conflict dialog appeared. Continuing standard import verification...")
                
            # 5. Wait for success or extract helpful partial-import failure errors/warnings from the UI
            try:
                # Wait for alert boxes OR Liferay's custom warning sheet (.sheet) to appear
                alert_selector = '.alert-success, .clay-alert-success, .alert-danger, .clay-alert-danger, .alert-warning, .sheet, div.sheet'
                page.wait_for_selector(alert_selector, timeout=25000)
                
                # Wait for any open modal dialogs or backdrop overlays to completely finish fading out and disappear
                try:
                    page.wait_for_selector('.modal-dialog, .modal-backdrop, .modal', state="hidden", timeout=5000)
                    page.wait_for_timeout(1000) # Safety pause to allow rendering to settle
                except Exception:
                    pass
                
                # Capture a clean screenshot of the active import result page showing success/error/warnings as a visual receipt
                screenshot_dir = os.path.join(os.getcwd(), 'tests', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, 'fragments-deployed.png')
                page.screenshot(path=screenshot_path)
                print(f"\nCreated deployment visual receipt showing import result at: {os.path.relpath(screenshot_path)}")
                
                # Check 1: Check for Liferay's custom warning/partial-success sheet (.sheet containing warning elements)
                warning_sheet = page.locator('div.sheet:has(.lexicon-icon-warning-full), div.sheet:has(.text-warning), div.sheet:has(.list-group)').first
                if warning_sheet.count() > 0:
                    # Extract warning heading
                    warning_heading = "Import Succeeded with Warnings"
                    heading_el = page.locator('.sheet span.text-warning, .sheet h1.text-warning, .sheet p.text-warning').first
                    if heading_el.count() > 0:
                        warning_heading = heading_el.text_content().strip()
                        
                    # Extract each list item warning details from the sidebar list group
                    warning_items = []
                    list_items = page.locator('.sheet li.list-group-item, .sheet .list-group-item').all()
                    for item in list_items:
                        try:
                            title_el = item.locator('.list-group-title').first
                            subtext_el = item.locator('.list-group-subtext').first
                            title = title_el.text_content().strip() if title_el.count() > 0 else "Unknown Fragment"
                            subtext = subtext_el.text_content().strip() if subtext_el.count() > 0 else "No details"
                            warning_items.append(f"  * {title}: {subtext}")
                        except Exception:
                            pass
                            
                    print("\n" + "=" * 80)
                    print(f"⚠️  [WARNING] [{collection_name}] {warning_heading}!")
                    print(f"    Liferay DXP Warning Sheet Extracted:")
                    print("-" * 80)
                    if warning_items:
                        print("\n".join(warning_items))
                    else:
                        print(warning_sheet.text_content().strip())
                    print("=" * 80 + "\n")
                    return False
                
                # Check 2: Check for danger/warning alerts in standard alert boxes
                danger_alert = page.locator('.alert-danger, .clay-alert-danger, .alert-warning').first
                if danger_alert.count() > 0:
                    error_msg = danger_alert.inner_text().strip()
                    print("\n" + "=" * 80)
                    print(f"❌  [ERROR] [{collection_name}] Import failed or was partially successful!")
                    print(f"    Helpful UI Error Message Extracted:")
                    print("-" * 80)
                    print(error_msg)
                    print("=" * 80 + "\n")
                    return False
                else:
                    print(f"[{collection_name}] Fragment Set imported successfully!")
                    
            except Exception as alert_err:
                print(f"Warning: [{collection_name}] Import complete, but did not detect standard success/error notifications: {alert_err}. Proceeding anyway.")
                
            # Let the state settle
            page.wait_for_timeout(1000)
            
        # Close context and browser
        context.close()
        browser.close()
        return True

def main():
    print("====================================================")
    print("        Liferay Page Fragments Deployer Script       ")
    print("====================================================")
    
    fragments_dir = get_fragments_dir()
    if not fragments_dir:
        print("Error: Could not find 'liferay/fragments/' directory. Please run this from the project root.")
        sys.exit(1)
        
    # 1. Scan for directories containing 'collection.json'
    collections = []
    for d in os.listdir(fragments_dir):
        full_path = os.path.join(fragments_dir, d)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, 'collection.json')):
            collections.append(d)
            
    if not collections:
        print("No custom fragment collections found under 'liferay/fragments/'.")
        sys.exit(0)
        
    print(f"Found {len(collections)} fragment collection(s): {', '.join(collections)}")
    
    # 2. Setup output folder (Using local .gitignore'd dist/ folder inside the workspace)
    deploy_assets_dir = os.path.join(os.getcwd(), 'liferay', 'dist')
    os.makedirs(deploy_assets_dir, exist_ok=True)
    
    # 3. Package each collection into workspace dist zip files
    success = True
    zipped_files = []
    for col in collections:
        source_path = os.path.join(fragments_dir, col)
        output_zip = os.path.join(deploy_assets_dir, f"{col}.zip")
        print(f"Packaging '{col}' into workspace dist: {output_zip}...")
        if package_fragments(source_path, output_zip):
            zipped_files.append(output_zip)
        else:
            success = False
            
    if not success:
        print("\nError: One or more fragment collections failed packaging.")
        sys.exit(1)
        
    # 4. Resolve Liferay Host & Credentials and Automate Frontend Import via Playwright
    email = env_utils.get_admin_email()
    password = env_utils.get_admin_password()
    host = env_utils.get_host()
    
    try:
        import_ok = automate_ui_import(host, email, password, zipped_files)
        if import_ok:
            print("\nPage Fragments deployed and imported into Global Site successfully!")
            sys.exit(0)
        else:
            print("\nError: Playwright automation failed to import Page Fragments.")
            sys.exit(1)
    except Exception as e:
        print(f"\nError: Automation failed during execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
