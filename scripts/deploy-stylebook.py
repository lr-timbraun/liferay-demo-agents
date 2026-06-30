#!/usr/bin/env python3
import os
import sys
import zipfile
import argparse
from playwright.sync_api import sync_playwright

# Import standard credential utility
sys.path.append(os.path.dirname(__file__))
import env_utils

def get_stylebooks_dir():
    """Locates the liferay/stylebooks folder in the workspace."""
    sb_path = os.path.join(os.getcwd(), 'liferay', 'stylebooks')
    return sb_path if os.path.exists(sb_path) else None

def package_stylebook(source_dir, output_zip):
    """
    Packages a Stylebook folder into a ZIP archive.
    The files must be nested inside a subdirectory (named after the Stylebook)
    inside the ZIP file to ensure Liferay's ZIP processor can resolve a unique key.
    """
    required_files = ["style-book.json", "frontend-tokens-values.json"]
    for f in required_files:
        if not os.path.exists(os.path.join(source_dir, f)):
            print(f"Error: Required file {f} missing in {source_dir}.")
            return False
            
    stylebook_folder_name = os.path.basename(source_dir.rstrip('/\\'))
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in required_files:
            file_path = os.path.join(source_dir, f)
            arcname = os.path.join(stylebook_folder_name, f)
            zipf.write(file_path, arcname=arcname)
    return True

def automate_ui_import(host, email, password, site_path, zipped_files):
    """Uses Playwright to log in and import packaged Style Book ZIP files into the target Liferay Site."""
    print("\n--- Initiating Playwright Browser Automation ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Login to Liferay
        print("Navigating to login page...")
        page.goto(f"{host}/c/portal/login")
        page.wait_for_load_state("networkidle")
        
        print(f"Logging in as agent: {email}...")
        page.locator('#_com_liferay_login_web_portlet_LoginPortlet_login').fill(email)
        page.locator('#_com_liferay_login_web_portlet_LoginPortlet_password').fill(password)
        page.locator('button[id*="LoginPortlet_"][type="submit"]').first.click()
        
        # Wait for Liferay's core theme marker indicating successful authentication on the body tag
        page.wait_for_selector('body.signed-in', timeout=20000)
        print("Login authenticated successfully!")
        page.wait_for_load_state("networkidle")
            
        # 2. Navigate to Target Site's Style Books Control Panel
        stylebooks_url = f"{host}/group/{site_path}/~/control_panel/manage/-/style_books/style_books"
        print(f"Navigating to target Site's Style Books Control Panel: {stylebooks_url}...")
        page.goto(stylebooks_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000) # Give extra time for React list data to render
        
        # 3. For each packaged stylebook, trigger the import
        for zip_path in zipped_files:
            sb_name = os.path.basename(zip_path).replace('.zip', '')
            print(f"\n[{sb_name}] Importing {zip_path} via UI...")
            
            # Find and click the Actions / Options button in Liferay's top Control Menu header (strictly data-qa-id and class-based, no text)
            options_btn = page.locator('li[data-qa-id="headerOptions"] button.portlet-options').first
            if options_btn.count() == 0:
                # Fallback selector in case of portal-header changes
                options_btn = page.locator('button[aria-label="Options"][title="Options"], button.portlet-options').first
                
            if options_btn.count() == 0:
                print(f"Error: Could not locate Options dropdown button on Style Books page. Saving screenshot.")
                page.screenshot(path="test-projects/stylebook-import-error-options.png")
                return False
                
            options_btn.click()
            
            # Click "Import" menuitem inside open dropdown (strictly data-action-based, targeting only the visible, verified element in the open dropdown)
            # Playwright will automatically wait up to 30 seconds for the dropdown to open and the element to become visible before clicking!
            import_menu_item = page.locator('.dropdown-menu button.dropdown-item[data-action*="StyleBookPortlet_import"]:visible, .dropdown-menu .dropdown-item[data-action*="import"]:visible').first
            import_menu_item.click()
            
            page.wait_for_timeout(1500) # Let the Import modal iframe load
            
            # Locate the Liferay import iframe dialog
            import_frame = page.frame_locator('iframe[title*="Import"]').first
            select_file_btn = import_frame.locator('input[type="file"], .form-control-file, .btn:has-text("Select File")').first
            if select_file_btn.count() == 0:
                print(f"Error: Could not locate file upload element inside Import dialog iframe. Saving screenshot.")
                page.screenshot(path="test-projects/stylebook-import-error-iframe.png")
                return False
                
            # Setup Playwright's file chooser event listener and click file upload
            with page.expect_file_chooser() as fc_info:
                select_file_btn.click()
            file_chooser = fc_info.value
            
            # Select the zip file
            file_chooser.set_files(zip_path)
            print(f"[{sb_name}] File uploaded to Import dialog.")
            
            # Click "Import" inside the iframe (Strictly class/type-based, no text)
            import_submit_btn = import_frame.locator('button.btn-primary, button[type="submit"]').first
            if import_submit_btn.count() == 0:
                print(f"Error: Could not locate primary Import button inside modal iframe. Saving screenshot.")
                page.screenshot(path="test-projects/stylebook-import-error-submit.png")
                return False
                
            import_submit_btn.click()
            print(f"[{sb_name}] Clicked Import. Waiting for Liferay processing...")
            
            # 4. Wait for success or extract helpful errors from inside the iframe
            try:
                alert_selector = '.alert-success, .clay-alert-success, .alert-danger, .clay-alert-danger, .alert-warning'
                import_frame.locator(alert_selector).first.wait_for(timeout=25000)
                
                # Check for danger/warning alerts inside the iframe
                danger_alert = import_frame.locator('.alert-danger, .clay-alert-danger, .alert-warning').first
                if danger_alert.count() > 0:
                    error_msg = danger_alert.text_content().strip()
                    print("\n" + "=" * 80)
                    print(f"❌  [ERROR] [{sb_name}] Stylebook import failed!")
                    print(f"    Helpful DXP Error Message Extracted:")
                    print("-" * 80)
                    print(error_msg)
                    print("=" * 80 + "\n")
                    return False
                else:
                    print(f"[{sb_name}] Style Book imported successfully!")
                    
            except Exception as alert_err:
                print(f"Warning: [{sb_name}] Alert check timed out: {alert_err}. Proceeding anyway.")
            
            # Close the modal dialog on the parent page (Strictly class-based, no text)
            close_btn = page.locator('.modal-dialog button.close, button.close, .modal-header button[class*="close"]').first
            if close_btn.count() > 0:
                close_btn.click()
            print(f"[{sb_name}] Modal closed.")
            page.wait_for_timeout(1000)
            
        # 5. Capture a clean screenshot of the imported books as a visual receipt
        screenshot_dir = os.path.join(os.getcwd(), 'tests', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, 'stylebooks-deployed.png')
        
        # Refresh to reload the list and show the books
        page.reload()
        page.wait_for_load_state("networkidle")
        page.screenshot(path=screenshot_path)
        print(f"\nCreated deployment visual receipt at: {os.path.relpath(screenshot_path)}")
        
        context.close()
        browser.close()
        return True

def main():
    print("====================================================")
    print("         Liferay Style Books Deployer Script        ")
    print("====================================================")
    
    parser = argparse.ArgumentParser(description="Liferay Style Books Deployer Script")
    parser.add_argument('--site', default='guest', help="The friendly URL path of the target Site (default: 'guest')")
    args = parser.parse_args()
    
    # Clean up site path (remove leading/trailing slashes)
    site_path = args.site.strip('/')
    
    sb_dir = get_stylebooks_dir()
    if not sb_dir:
        print("Error: Could not find 'liferay/stylebooks/' directory. Please run this from the project root.")
        sys.exit(1)
        
    # 1. Scan for subdirectories containing 'style-book.json'
    books = [d for d in os.listdir(sb_dir) if os.path.isdir(os.path.join(sb_dir, d)) and os.path.exists(os.path.join(sb_dir, d, 'style-book.json'))]
    if not books:
        print("No custom Style Books found under 'liferay/stylebooks/'.")
        sys.exit(0)
        
    print(f"Found {len(books)} Style Book(s): {', '.join(books)}")
    
    # 2. Setup output folder (Using local .gitignore'd dist/ folder inside the workspace)
    deploy_assets_dir = os.path.join(os.getcwd(), 'liferay', 'dist')
    os.makedirs(deploy_assets_dir, exist_ok=True)
    
    # 3. Package each Stylebook folder into dist/
    success = True
    zipped_files = []
    for b in books:
        source_path = os.path.join(sb_dir, b)
        output_zip = os.path.join(deploy_assets_dir, f"{b}.zip")
        print(f"Packaging '{b}' -> {output_zip}...")
        if package_stylebook(source_path, output_zip):
            zipped_files.append(output_zip)
        else:
            success = False
            
    if not success or not zipped_files:
        print("\nError: One or more Style Books failed packaging.")
        sys.exit(1)
        
    # 4. Resolve Liferay Host & Credentials and Automate Frontend Import via Playwright
    email = env_utils.get_admin_email()
    password = env_utils.get_admin_password()
    host = env_utils.get_host()
    
    try:
        import_ok = automate_ui_import(host, email, password, site_path, zipped_files)
        if import_ok:
            print("\nStyle Books deployed and imported into target Site successfully!")
            sys.exit(0)
        else:
            print("\nError: Playwright automation failed to import Style Books.")
            sys.exit(1)
    except Exception as e:
        print(f"\nError: Automation failed during execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
