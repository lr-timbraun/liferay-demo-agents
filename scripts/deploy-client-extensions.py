#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def is_npm_available():
    """Checks if `npm` is available in the system path."""
    return shutil.which('npm') is not None

def get_client_extensions_dir():
    """Locates the client-extensions folder in the Liferay workspace."""
    cwd = os.getcwd()
    cx_path = os.path.join(cwd, 'liferay', 'client-extensions')
    if os.path.exists(cx_path):
        return cx_path
    return None

def build_client_extension(cx_dir, project_name):
    """Compiles a specific client extension locally if it's node-based."""
    project_path = os.path.join(cx_dir, project_name)
    package_json = os.path.join(project_path, 'package.json')
    
    if not os.path.exists(package_json):
        # Not a node-based client extension, skipping local build
        return True
        
    print(f"\n--- Building React Client Extension: {project_name} ---")
    if not is_npm_available():
        print("Warning: Local 'npm' command not found in your system PATH.")
        print("Bypassing local compilation; LDM container will attempt to compile it during deploy.")
        return True
        
    try:
        # Run npm install
        print(f"[{project_name}] Running 'npm install'...")
        # Use shell=True on Windows to resolve the .cmd extension for npm automatically
        use_shell = sys.platform == 'win32'
        subprocess.run(['npm', 'install'], cwd=project_path, shell=use_shell, check=True)
        
        # Run npm run build
        print(f"[{project_name}] Running 'npm run build'...")
        subprocess.run(['npm', 'run', 'build'], cwd=project_path, shell=use_shell, check=True)
        
        # Verify build output
        build_dir = os.path.join(project_path, 'build')
        if os.path.exists(build_dir):
            print(f"[{project_name}] Local compilation completed successfully.")
            return True
        else:
            print(f"Error: [{project_name}] Build completed but 'build/' folder was not found.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: [{project_name}] Compilation failed during '{e.cmd[0]}'.")
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
    
    # 2. Compile each project locally if package.json is present
    success = True
    for project in projects:
        if not build_client_extension(cx_dir, project):
            success = False
            
    if not success:
        print("\nError: Local compilation failed for one or more client extensions.")
        print("Aborting deploy to prevent deploying broken/incomplete assets.")
        sys.exit(1)
        
    # 3. Invoke LDM Deploy to copy and hot-deploy the built assets
    print("\n--- Synchronizing and Deploying via LDM ---")
    try:
        # We run 'ldm deploy' from the current project root directory
        print("Running 'ldm deploy'...")
        subprocess.run(['ldm', 'deploy'], shell=sys.platform == 'win32', check=True)
        print("\nLiferay Client Extensions Deployment Completed Successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nError: 'ldm deploy' failed during execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
