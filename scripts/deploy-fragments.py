#!/usr/bin/env python3
import os
import sys
import zipfile

def get_workspace_dir():
    """Returns the main project root directory."""
    return os.getcwd()

def get_fragments_dir():
    """Locates the liferay/fragments folder in the workspace."""
    cwd = get_workspace_dir()
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

def main():
    print("====================================================")
    print("        Liferay Page Fragments Packager Script       ")
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
        
    # 4. Print beautiful, explicit step-by-step UI import instructions
    print("\n====================================================")
    print("🎉 PAGE FRAGMENTS PACKAGING COMPLETE!")
    print("====================================================")
    print("Because Liferay does not expose a public API for fragment imports,")
    print("you must import them manually via the user interface.")
    print("\n👉 Follow these steps to import your Fragment Sets GLOBALLY:")
    print("------------------------------------------------------------")
    print("1. Log in to your Liferay instance as an Administrator.")
    print("2. Open the Site Selector (top-left menu) and click on the 'Global' site.")
    print("   * Note: Importing into the Global site makes fragments immediately available")
    print("     across all other demo and client-facing sites!")
    print("3. In the left-hand navigation sidebar, go to:")
    print("   Design  ->  Fragments (or Page Fragments)")
    print("4. In the top-right corner of the Page Fragments page, click the 'Actions'")
    print("   ellipsis (vertical three dots) or 'Import' button, and select 'Import'.")
    print("5. Browse and select the packaged ZIP file(s) from your local deploy-assets path:")
    for f in zipped_files:
        print(f"   📂 {os.path.relpath(f)}")
    print("6. Click 'Import'.")
    print("7. Done! The fragments are imported and fully ready to be placed onto pages.")
    print("====================================================\n")

if __name__ == '__main__':
    main()
