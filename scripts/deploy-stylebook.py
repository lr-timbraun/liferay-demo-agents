#!/usr/bin/env python3
import os
import sys
import zipfile
import base64
from playwright.sync_api import sync_playwright

# Import standard credential utility
sys.path.append(os.path.dirname(__file__))
import env_utils

def get_workspace_dir():
    """Returns the main project root directory."""
    return os.getcwd()

def get_stylebooks_dir():
    """Locates the liferay/stylebooks folder in the workspace."""
    cwd = get_workspace_dir()
    sb_path = os.path.join(cwd, 'liferay', 'stylebooks')
    if os.path.exists(sb_path):
        return sb_path
    return None

def package_stylebook(source_dir, output_zip):
    """
    Packages a Stylebook folder into a ZIP archive.
    Only style-book.json and frontend-tokens-values.json are written at the root.
    """
    required_files = ["style-book.json", "frontend-tokens-values.json"]
    
    # Check if files exist
    for f in required_files:
        if not os.path.exists(os.path.join(source_dir, f)):
            print(f"Error: Required file {f} missing in {source_dir}.")
            return False
            
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in required_files:
            file_path = os.path.join(source_dir, f)
            zipf.write(file_path, arcname=f)
    return True

def automate_ui_import(host, email, password, zipped_files):
    """Uses Playwright to log in and import packaged Style Book ZIP files into the target Liferay Site."""
    print("\n--- Initiating Playwright Browser Automation ---")
    
    # Enable unverified SSL contexts inside python's subprocess/browser environment if needed
    os.environ['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
    
    with sync_playwright() as p:
        # Launch Chromium headlessly
        print("Launching headless Chromium browser...")
        browser = p.chromium.launch(headless=True)
        
        # Create context with unverified SSL context to bypass self-signed Traefik proxy cert errors
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        # 1. Login to Liferay
        login_url = f"{host}/c/portal/login"
        print(f"Navigating to login page: {login_url}...")
        page.goto(login_url)
        page.wait_for_load_state("networkidle")
        
        # Specific login input IDs
        login_input = page.locator('#_com_liferay_login_web_portlet_LoginPortlet_login')
        password_input = page.locator('#_com_liferay_login_web_portlet_LoginPortlet_password')
        
        if login_input.count() > 0:
            print(f"Logging in as: {email}...")
            login_input.fill(email)
            password_input.fill(password)
            
            # Click Sign In (Specifically LoginPortlet submit button)
            submit_btn = page.locator('button[id*="LoginPortlet_"][type="submit"]').first
            submit_btn.click()
            
            print("Credentials submitted. Waiting for authenticated landing page...")
            try:
                # Wait for standard authenticated UI elements (avatar, admin panel, or product menu)
                page.wait_for_selector('.user-avatar, .control-menu, .lfr-product-menu-panel', timeout=20000)
                print("Login authenticated successfully!")
            except Exception:
                print("Warning: Timed out waiting for standard admin selectors. Checking page URL...")
                print("Current page URL:", page.url)
                
            page.wait_for_load_state("networkidle")
            
        # 2. Navigate to Target Site's Style Books Control Panel
        # Stylebooks must be uploaded to the specific site they are used on, e.g. /group/guest/ (or custom site friendly URL)
        stylebooks_url = f"{host}/group/guest/~/control_panel/manage/-/style_books/style_books"
        print(f"Navigating to target Site's Style Books Control Panel: {stylebooks_url}...")
        page.goto(stylebooks_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000) # Give extra time for React/JS list data to render
        
        # 3. For each packaged stylebook, trigger the import
        for zip_path in zipped_files:
            sb_name = os.path.basename(zip_path).replace('.zip', '')
            print(f"\n[{sb_name}] Attempting to import {zip_path} via UI...")
            
            # Trigger Options dropdown
            options_btn = page.get_by_role("button", name="Options").first
            if options_btn.count() == 0:
                # Fallback selector in case of non-standard button text or icon
                options_btn = page.locator('button[id*="Options"], button[class*="options"], button[data-toggle="dropdown"]:has(.lexicon-icon-ellipsis-v)').first
                
            if options_btn.count() == 0:
                print(f"Error: Could not locate Options dropdown button on Style Books page. Taking failure screenshot.")
                page.screenshot(path="liferay/deploy-assets/stylebook-import-error-options.png")
                return False
                
            options_btn.click()
            page.wait_for_timeout(500) # Let dropdown slide open
            
            # Click "Import" menuitem
            import_menu_item = page.get_by_role("menuitem", name="Import", exact=True).first
            if import_menu_item.count() == 0:
                import_menu_item = page.locator('a.dropdown-item:has-text("Import"), .dropdown-menu button:has-text("Import"), .dropdown-menu a:has-text("Import")').first
                
            if import_menu_item.count() == 0:
                print(f"Error: Could not find 'Import' option in Options dropdown. Taking failure screenshot.")
                page.screenshot(path="liferay/deploy-assets/stylebook-import-error-menu.png")
                return False
                
            import_menu_item.click()
            page.wait_for_timeout(1500) # Let the Import modal iframe load
            
            # Locate the Liferay import iframe dialog
            import_frame = page.frame_locator('iframe[title*="Import"]')
            select_file_btn = import_frame.get_by_label("Select File").first
            if select_file_btn.count() == 0:
                select_file_btn = import_frame.locator('input[type="file"], .form-control-file, .btn:has-text("Select File")').first
                
            if select_file_btn.count() == 0:
                print(f"Error: Could not locate 'Select File' button inside Liferay's Import dialog iframe. Saving screenshot.")
                page.screenshot(path="liferay/deploy-assets/stylebook-import-error-iframe.png")
                return False
                
            # Setup Playwright's file chooser event listener
            with page.expect_file_chooser() as fc_info:
                select_file_btn.click()
            file_chooser = fc_info.value
            
            # Select the zip file
            file_chooser.set_files(zip_path)
            print(f"[{sb_name}] File uploaded to Import dialog.")
            
            # Click "Import" inside the iframe
            import_submit_btn = import_frame.get_by_role("button", name="Import").first
            if import_submit_btn.count() == 0:
                import_submit_btn = import_frame.locator('button[type="submit"], .btn-primary').first
                
            import_submit_btn.click()
            print(f"[{sb_name}] Clicked Import. Processing...")
            page.wait_for_timeout(2000) # Wait for DXP processing
            
            # Close the modal on the parent page
            close_btn = page.get_by_label("Import").get_by_label("Close", exact=True).first
            if close_btn.count() == 0:
                close_btn = page.locator('button.close, .modal-header button[class*="close"]').first
                
            if close_btn.count() > 0:
                close_btn.click()
            print(f"[{sb_name}] Import complete.")
            page.wait_for_timeout(1000)
            
        # 4. Capture a clean screenshot of the imported books as a visual receipt
        screenshot_dir = os.path.join(get_workspace_dir(), 'tests', 'screenshots')
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
    
    sb_dir = get_stylebooks_dir()
    if not sb_dir:
        print("Error: Could not find 'liferay/stylebooks/' directory. Please run this from the project root.")
        sys.exit(1)
        
    # 1. Scan for subdirectories containing 'style-book.json'
    books = []
    for d in os.listdir(sb_dir):
        full_path = os.path.join(sb_dir, d)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, 'style-book.json')):
            books.append(d)
            
    if not books:
        print("No custom Style Books found under 'liferay/stylebooks/'.")
        sys.exit(0)
        
    print(f"Found {len(books)} Style Book(s): {', '.join(books)}")
    
    # 2. Setup output folder (Using LDM's standard root-level deploy/ directory)
    deploy_assets_dir = os.path.join(get_workspace_dir(), 'deploy')
    os.makedirs(deploy_assets_dir, exist_ok=True)
    
    # 3. Package each Stylebook folder into deploy-assets/
    success = True
    zipped_files = []
    for b in books:
        source_path = os.path.join(sb_dir, b)
        output_zip = os.path.join(deploy_assets_dir, f"{b}.zip")
        print(f"Packaging '{b}' into {output_zip}...")
        if package_stylebook(source_path, output_zip):
            zipped_files.append(output_zip)
        else:
            success = False
            
    if not success:
        print("\nError: One or more Style Books failed packaging.")
        sys.exit(1)
        
    # 4. Resolve Liferay Host & Credentials and Automate Frontend Import via Playwright
    email = env_utils.get_admin_email()
    password = env_utils.get_admin_password()
    host = env_utils.get_host()
    
    try:
        import_ok = automate_ui_import(host, email, password, zipped_files)
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
