#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import zipfile

def is_npm_available():
    """Checks if `npm` is available in the system path."""
    return shutil.which('npm') is not None

def get_workspace_dir():
    """Returns the main project root directory."""
    return os.getcwd()

def get_client_extensions_dir():
    """Locates the liferay/client-extensions folder in the workspace."""
    cwd = get_workspace_dir()
    cx_path = os.path.join(cwd, 'liferay', 'client-extensions')
    if os.path.exists(cx_path):
        return cx_path
    return None

def build_client_extension(cx_dir, project_name):
    """Compiles a specific client extension locally if it has a package.json."""
    project_path = os.path.join(cx_dir, project_name)
    package_json = os.path.join(project_path, 'package.json')
    
    if not os.path.exists(package_json):
        # Not a node-based client extension, nothing to compile locally
        return True
        
    print(f"\n[{project_name}] Compiling node-based assets locally...")
    if not is_npm_available():
        print(f"Warning: Local 'npm' command not found. Skipping local compilation for {project_name}.")
        return True
        
    try:
        use_shell = sys.platform == 'win32'
        
        # 1. Run npm install
        print(f"[{project_name}] Running 'npm install'...")
        subprocess.run(['npm', 'install'], cwd=project_path, shell=use_shell, check=True)
        
        # 2. Run npm run build
        print(f"[{project_name}] Running 'npm run build'...")
        subprocess.run(['npm', 'run', 'build'], cwd=project_path, shell=use_shell, check=True)
        
        build_dir = os.path.join(project_path, 'build')
        if os.path.exists(build_dir):
            print(f"[{project_name}] Local compilation successful.")
            return True
        else:
            print(f"Error: [{project_name}] Build completed but 'build/' folder was not found.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: [{project_name}] Compilation failed: {e}")
        return False

def package_and_copy_client_extension(cx_dir, project_name):
    """Packages the client extension files into a Liferay-compatible .zip archive and copies it to LDM's client-extensions directory."""
    project_path = os.path.join(cx_dir, project_name)
    yaml_path = os.path.join(project_path, 'client-extension.yaml')
    
    if not os.path.exists(yaml_path):
        print(f"Error: [{project_name}] client-extension.yaml is missing.")
        return False
        
    # LDM's root-level directory for deploying client extensions
    root_cx_deploy_dir = os.path.join(get_workspace_dir(), 'client-extensions')
    os.makedirs(root_cx_deploy_dir, exist_ok=True)
    
    output_zip_path = os.path.join(root_cx_deploy_dir, f"{project_name}.zip")
    print(f"[{project_name}] Packaging client extension into {output_zip_path}...")
    
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 1. Add client-extension.yaml at the root of the archive
            zipf.write(yaml_path, 'client-extension.yaml')
            
            # 2. Package static assets (handling build/static or assets directories)
            package_json = os.path.join(project_path, 'package.json')
            
            if os.path.exists(package_json):
                # Node-based client extensions: Map build/static/* to static/* (matches "assemble: - from: build/static into: static")
                build_static_dir = os.path.join(project_path, 'build', 'static')
                build_dir = os.path.join(project_path, 'build')
                
                source_dir = None
                zip_prefix = "static"
                
                if os.path.exists(build_static_dir):
                    source_dir = build_static_dir
                elif os.path.exists(build_dir):
                    source_dir = build_dir
                    
                if source_dir:
                    for root, _, files in os.walk(source_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Reconstruct relative path inside the zip file
                            rel_path = os.path.relpath(file_path, source_dir)
                            archive_path = os.path.join(zip_prefix, rel_path)
                            zipf.write(file_path, archive_path)
                else:
                    print(f"Warning: No compiled 'build/' folder found for {project_name}. Packaging empty assets.")
            else:
                # Non-node-based client extensions (e.g. batch, config, theme-css)
                # Package all contents except workspace config files
                exclude_files = {'client-extension.yaml', 'bnd.bnd', 'package.json', 'package-lock.json'}
                for root, _, files in os.walk(project_path):
                    for file in files:
                        if file in exclude_files:
                            continue
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, project_path)
                        zipf.write(file_path, rel_path)
                        
        print(f"[{project_name}] Successfully packaged and deployed to LDM root client-extensions/ directory.")
        return True
    except Exception as e:
        print(f"Error packaging {project_name}: {e}")
        return False

def main():
    print("====================================================")
    print("     Liferay Client Extensions Deployer Script      ")
    print("====================================================")
    
    cx_dir = get_client_extensions_dir()
    if not cx_dir:
        print("Error: Could not find 'liferay/client-extensions/' directory. Please run this from the project root.")
        sys.exit(1)
        
    # 1. Scan client extensions
    projects = [d for d in os.listdir(cx_dir) if os.path.isdir(os.path.join(cx_dir, d)) and os.path.exists(os.path.join(cx_dir, d, 'client-extension.yaml'))]
    
    if not projects:
        print("No custom client extensions found under 'liferay/client-extensions/'.")
        sys.exit(0)
        
    print(f"Found {len(projects)} client extension(s): {', '.join(projects)}")
    
    # 2. Compile node-based client extensions
    build_success = True
    for project in projects:
        if not build_client_extension(cx_dir, project):
            build_success = False
            
    if not build_success:
        print("\nError: Local compilation failed for one or more client extensions.")
        print("Aborting deploy to prevent deploying broken/incomplete assets.")
        sys.exit(1)
        
    # 3. Package as .zip and copy directly to LDM's hot-deploy path
    print("\n--- Packaging and Hot-Deploying to LDM ---")
    deploy_success = True
    for project in projects:
        if not package_and_copy_client_extension(cx_dir, project):
            deploy_success = False
            
    if deploy_success:
        print("\nAll Liferay Client Extensions deployed successfully and ready for use!")
        sys.exit(0)
    else:
        print("\nError: One or more client extensions failed deployment packaging.")
        sys.exit(1)

if __name__ == '__main__':
    main()
