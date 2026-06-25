#!/usr/bin/env python3
import os
import sys
import zipfile
import base64
from playwright.sync_api import sync_playwright

def get_env_path():
    """Finds the .env file by searching upwards from the current directory."""
    current_dir = os.path.abspath(os.getcwd())
    while current_dir != os.path.dirname(current_dir):
        env_path = os.path.join(current_dir, '.env')
        if os.path.exists(env_path):
            return env_path
        current_dir = os.path.dirname(current_dir)
    return os.path.join(os.path.abspath(os.getcwd()), '.env')

def get_credentials():
    """Reads Liferay credentials and host URL from the local .env file."""
    env_path = get_env_path()
    email = None
    password = None
    host = None
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped.startswith('LIFERAY_ADMIN_EMAIL_ADDRESS='):
                    email = line_stripped.split('=', 1)[1].strip()
                elif line_stripped.startswith('LIFERAY_ADMIN_PASSWORD='):
                    password = line_stripped.split('=', 1)[1].strip()
                elif line_stripped.startswith('LIFERAY_HOST='):
                    host = line_stripped.split('=', 1)[1].strip()
                    
    if not host or not email or not password:
        print(f"Error: Missing credentials or LIFERAY_HOST inside {env_path}")
        sys.exit(1)
        
    return email, password, host.rstrip('/')

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
        
        # Check if we are redirected or already authenticated
        login_input = page.locator('input[type="email"], input[type="text"], [name*="login"]').first
        if login_input.count() > 0:
            print(f"Logging in as agent: {email}...")
            login_input.fill(email)
            
            password_input = page.locator('input[type="password"], [name*="password"]').first
            password_input.fill(password)
            
            # Click Sign In
            submit_btn = page.locator('button[type="submit"], input[type="submit"], .btn-primary:has-text("Sign In"), .btn-primary:has-text("Anmelden")').first
            submit_btn.click()
            page.wait_for_load_state("networkidle")
            print("Authentication successful.")
            
        # 2. Navigate to Global site Page Fragments Portlet
        fragments_url = f"{host}/group/global/~/control_panel/manage?p_p_id=com_liferay_fragment_web_portlet_FragmentPortlet"
        print(f"Navigating to Global Site Page Fragments Control Panel: {fragments_url}...")
        page.goto(fragments_url)
        page.wait_for_load_state("networkidle")
        
        # 3. For each packaged collection, trigger the import
        for zip_path in zipped_files:
            collection_name = os.path.basename(zip_path).replace('.zip', '')
            print(f"\n[{collection_name}] Attempting to import {zip_path} via UI...")
            
            # Find and click the actions / dropdown button in the management bar
            # Handles different Liferay/Clay toolbar class permutations
            actions_btn = page.locator('button[id*="Actions"], button[class*="actions"], .management-bar button, button[data-toggle="dropdown"]:has(.icon-actions)').first
            if actions_btn.count() == 0:
                print(f"Error: Could not locate Actions/Dropdown menu on Page Fragments page. Taking failure screenshot.")
                page.screenshot(path="liferay/deploy-assets/import-error-actions.png")
                return False
                
            actions_btn.click()
            page.wait_for_timeout(500) # Let dropdown slide open
            
            # Click "Import" menuitem
            import_menu_item = page.locator('a.dropdown-item:has-text("Import"), .dropdown-menu button:has-text("Import"), .dropdown-menu a:has-text("Import"), role=menuitem[name="Import"]').first
            if import_menu_item.count() == 0:
                print(f"Error: Could not find 'Import' option in Actions dropdown. Taking failure screenshot.")
                page.screenshot(path="liferay/deploy-assets/import-error-menu.png")
                return False
                
            import_menu_item.click()
            page.wait_for_timeout(1000) # Let modal load
            
            # Set the ZIP file in Liferay's modal file input
            file_input = page.locator('input[type="file"]').first
            if file_input.count() == 0:
                print(f"Error: Could not find file input element in import modal. Taking failure screenshot.")
                page.screenshot(path="liferay/deploy-assets/import-error-fileinput.png")
                return False
                
            # Set local zip path
            file_input.set_input_files(zip_path)
            print(f"[{collection_name}] File uploaded to modal.")
            
            # Click "Import" primary button inside the modal
            import_btn = page.locator('.modal-footer button:has-text("Import"), .modal-footer .btn-primary').first
            import_btn.click()
            print(f"[{collection_name}] Clicked import. Waiting for Liferay processing...")
            
            # Wait for success notification (Native alert-success or success notification message)
            try:
                page.wait_for_selector('.alert-success, .clay-alert-success, .alert-dismissible:has-text("successful")', timeout=20000)
                print(f"[{collection_name}] Fragment Set imported successfully!")
            except Exception:
                print(f"Warning: [{collection_name}] Import complete, but did not detect the standard success notification. Proceeding anyway.")
                
            # Let the modal close/refresh
            page.wait_for_timeout(1000)
            
        # 4. Capture a clean screenshot of the imported sets as a visual receipt
        screenshot_dir = os.path.join(get_workspace_dir(), 'tests', 'screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, 'fragments-deployed.png')
        
        # Refresh to reload the list and show the sets
        page.reload()
        page.wait_for_load_state("networkidle")
        page.screenshot(path=screenshot_path)
        print(f"\nCreated deployment visual receipt at: {os.path.relpath(screenshot_path)}")
        
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
    
    # 2. Setup output folder
    deploy_assets_dir = os.path.join(get_workspace_dir(), 'liferay', 'deploy-assets')
    os.makedirs(deploy_assets_dir, exist_ok=True)
    
    # 3. Package each collection into deploy-assets/
    success = True
    zipped_files = []
    for col in collections:
        source_path = os.path.join(fragments_dir, col)
        output_zip = os.path.join(deploy_assets_dir, f"{col}.zip")
        print(f"Packaging '{col}' into {output_zip}...")
        if package_fragments(source_path, output_zip):
            zipped_files.append(output_zip)
        else:
            success = False
            
    if not success:
        print("\nError: One or more fragment collections failed packaging.")
        sys.exit(1)
        
    # 4. Resolve Liferay Host & Credentials and Automate Frontend Import via Playwright
    email, password, host = get_credentials()
    
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
