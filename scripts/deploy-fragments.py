#!/usr/bin/env python3
import os
import sys
import zipfile
from playwright.sync_api import sync_playwright

# Import standard credentials
sys.path.append(os.path.dirname(__file__))
import env_utils

def get_fragments_dir():
    """Locates the liferay/fragments folder in the workspace."""
    fragments_path = os.path.join(os.getcwd(), 'liferay', 'fragments')
    return fragments_path if os.path.exists(fragments_path) else None

def package_fragments(collection_dir, output_zip):
    """Packages a Liferay Fragment Collection into a compliant ZIP file."""
    collection_root_name = os.path.basename(collection_dir.rstrip('/\\'))
    if not os.path.exists(os.path.join(collection_dir, 'collection.json')):
        print(f"Error: Mandatory 'collection.json' missing in {collection_dir}")
        return False
        
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(collection_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(collection_root_name, os.path.relpath(file_path, collection_dir))
                zipf.write(file_path, arcname=arcname)
    return True

def automate_ui_import(host, email, password, zipped_files):
    """Uses Playwright to log in and import packaged Fragment ZIP files into the Global Site."""
    print("\n--- Initiating Playwright Browser Automation ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Login
        print(f"Navigating to login page...")
        page.goto(f"{host}/c/portal/login")
        page.wait_for_load_state("networkidle")
        
        print(f"Logging in as agent: {email}...")
        page.locator('#_com_liferay_login_web_portlet_LoginPortlet_login').fill(email)
        page.locator('#_com_liferay_login_web_portlet_LoginPortlet_password').fill(password)
        page.locator('button[id*="LoginPortlet_"][type="submit"]').first.click()
        
        # Wait for authentication body class
        page.wait_for_selector('body.signed-in', timeout=20000)
        print("Login authenticated successfully!")
        page.wait_for_load_state("networkidle")
            
        # 2. Go to Fragments Page
        fragments_url = f"{host}/group/global/~/control_panel/manage/-/fragments/fragment_collections"
        print(f"Navigating to Page Fragments Panel...")
        page.goto(fragments_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # 3. Sequentially import each collection
        for zip_path in zipped_files:
            collection_name = os.path.basename(zip_path).replace('.zip', '')
            print(f"\n[{collection_name}] Importing {zip_path}...")
            
            # Click Actions / Options button
            actions_btn = page.locator('#portlet_com_liferay_fragment_web_portlet_FragmentPortlet button[title*="Fragment Sets Options"], #portlet_com_liferay_fragment_web_portlet_FragmentPortlet button[title="Fragment Sets Options"]').first
            if actions_btn.count() == 0:
                print("Error: Could not locate Actions/Dropdown button.")
                return False
            actions_btn.click()
            page.wait_for_timeout(500)
            
            # Click "Import" menuitem
            import_menu_item = page.locator('.dropdown-menu a.dropdown-item[icon="import"], .dropdown-menu a[href*="view_import"]').first
            if import_menu_item.count() == 0:
                print("Error: Could not find 'Import' option in dropdown.")
                return False
            import_menu_item.click()
            
            # Sub-page file selection and submit
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            
            file_input = page.locator('input[type="file"]').first
            if file_input.count() == 0:
                print("Error: Could not find file input element.")
                return False
                
            file_input.set_input_files(zip_path)
            
            import_btn = page.locator('.tbar button.btn-primary, .tbar .btn-primary').first
            if import_btn.count() == 0:
                print("Error: Could not find primary Import button.")
                return False
            import_btn.click()
            print(f"[{collection_name}] Upload submitted. Waiting for processing...")
            
            # 4. Handle duplication conflict modal if it appears
            try:
                modal_selector = '.modal-dialog:has-text("Manage Existing Items"), .modal-dialog:has(input[value="overwrite"])'
                page.wait_for_selector(modal_selector, timeout=4000)
                print(f"[{collection_name}] Conflict detected! Selecting 'Overwrite Existing Items'...")
                page.locator('.modal-dialog input[type="radio"][value="overwrite"]').first.click()
                page.locator('.modal-dialog .modal-footer button.btn-primary, .modal-dialog .modal-footer .btn-primary').first.click()
                print(f"[{collection_name}] Overwrite conflict resolved.")
            except Exception:
                pass
                
            # 5. Wait for success/warning alert states
            try:
                alert_selector = '.alert-success, .clay-alert-success, .alert-danger, .clay-alert-danger, .alert-warning, .sheet, div.sheet'
                page.wait_for_selector(alert_selector, timeout=25000)
                
                # Wait for any active modal to completely fade out before capturing screenshot
                try:
                    page.wait_for_selector('.modal-dialog, .modal-backdrop, .modal', state="hidden", timeout=4000)
                    page.wait_for_timeout(1000)
                except Exception:
                    pass
                
                # Save visual receipt screenshot
                screenshot_dir = os.path.join(os.getcwd(), 'tests', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                page.screenshot(path=os.path.join(screenshot_dir, 'fragments-deployed.png'))
                
                # Check 1: Check for Liferay's custom import result sheet (.sheet)
                sheet_el = page.locator('div.sheet .panel').first
                if sheet_el.count() > 0:
                    # Determine if it is a Success or Warning sheet
                    is_warning = page.locator('div.sheet .text-warning, div.sheet .lexicon-icon-warning-full').count() > 0
                    
                    # Extract the main result heading dynamically (using the exact class from the dump)
                    heading = "Import Succeeded"
                    heading_el = page.locator('div.sheet .text-success, div.sheet .text-warning').first
                    if heading_el.count() > 0:
                        heading = heading_el.text_content().strip()
                        
                    # Extract the list of imported items
                    summary_items = []
                    list_items = page.locator('div.sheet li.list-group-item').all()
                    for item in list_items:
                        title_el = item.locator('.list-group-title').first
                        title = title_el.text_content().strip() if title_el.count() > 0 else "Unknown"
                        
                        # Warnings have a subtext detailing the issue. Successes do not.
                        subtext_el = item.locator('.list-group-subtext').first
                        if subtext_el.count() > 0:
                            subtext = subtext_el.text_content().strip()
                            summary_items.append(f"  * {title}: {subtext}")
                        else:
                            summary_items.append(f"  * {title}")
                            
                    print("\n" + "=" * 80)
                    if is_warning:
                        print(f"⚠️  [WARNING] [{collection_name}] {heading}!")
                        print("-" * 80)
                        print("\n".join(summary_items))
                        print("=" * 80 + "\n")
                        return False
                    else:
                        print(f"✅  [SUCCESS] [{collection_name}] {heading}!")
                        print("-" * 80)
                        print("\n".join(summary_items))
                        print("=" * 80 + "\n")
                        return True
                
                # Check for standard error alerts
                danger_alert = page.locator('.alert-danger, .clay-alert-danger, .alert-warning').first
                if danger_alert.count() > 0:
                    print(f"\n❌  [ERROR] [{collection_name}] Import failed!\n" + "-"*80 + f"\n{danger_alert.inner_text().strip()}\n" + "="*80 + "\n")
                    return False
                else:
                    print(f"[{collection_name}] Fragment Set imported successfully!")
                    
            except Exception as alert_err:
                print(f"Warning: [{collection_name}] Alert check timed out: {alert_err}")
                
            page.wait_for_timeout(1000)
            
        context.close()
        browser.close()
        return True

def main():
    print("====================================================")
    print("        Liferay Page Fragments Deployer Script       ")
    print("====================================================")
    
    fragments_dir = get_fragments_dir()
    if not fragments_dir:
        print("Error: Could not find 'liferay/fragments/' directory. Run from project root.")
        sys.exit(1)
        
    collections = [d for d in os.listdir(fragments_dir) if os.path.isdir(os.path.join(fragments_dir, d)) and os.path.exists(os.path.join(fragments_dir, d, 'collection.json'))]
    if not collections:
        print("No custom fragment collections found.")
        sys.exit(0)
        
    print(f"Found {len(collections)} collection(s): {', '.join(collections)}")
    
    deploy_assets_dir = os.path.join(os.getcwd(), 'liferay', 'dist')
    os.makedirs(deploy_assets_dir, exist_ok=True)
    
    zipped_files = []
    success = True
    for col in collections:
        output_zip = os.path.join(deploy_assets_dir, f"{col}.zip")
        print(f"Packaging '{col}' -> {output_zip}...")
        if package_fragments(os.path.join(fragments_dir, col), output_zip):
            zipped_files.append(output_zip)
        else:
            success = False
            
    if not success or not zipped_files:
        print("\nError: Packaging failed.")
        sys.exit(1)
        
    try:
        import_ok = automate_ui_import(env_utils.get_host(), env_utils.get_admin_email(), env_utils.get_admin_password(), zipped_files)
        if import_ok:
            print("\nPage Fragments deployed successfully!")
            sys.exit(0)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: Automation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
